# This file is for the purposes of:
# - Receiving UDP packets from the controller
# - Controlling the tank's DC and Servo motors using input from the UDP packets

###########
# Imports #
###########
from motor_driver import DCMotor
from servo_driver import Servo
from time import sleep
from datetime import datetime
from variables import *
import socket as s
import json

##############
# Parameters #
##############
# Motor Driver
AIN1 = x
AIN2 = x
PWMA = x
BIN1 = x
BIN2 = x
PWMB = x
STBY = x
# Servo
PWM = x
# UDP
tank_rx_port = x

##################
# Initialization #
##################
left_motor = DCMotor(AIN1, AIN2, PWMA, STBY) # Motor(IN1,IN2,PWM,STANDBY,(Reverse polarity?))
right_motor = DCMotor(BIN1, BIN2, PWMB, STBY)
left_motor.standby(True)
right_motor.standby(True)
servo = Servo(PWM, init_angle=90)

########
# Main #
########
'''
Pseudo-code for this file
-------------------------

Make socket connecting to controller via UDP

Wait to recieve UDP packet from controller
Set DC motor speeds
Set Servo angle
If fired
  do firing stuff
'''

# Setup UDP #
tank_socket = s.socket(s.AF_INET, s.SOCK_DGRAM) # Create UDP socket
tank_address = ('localhost', tank_rx_port) # Bind the socket to an address and port
tank_socket.bind(tank_address)
print("UDP server is up and listening...")

# Main control loop #
try:
  while True:
    # Recieve UDP packet from controller #
    data, controller_address = tank_socket.recvfrom(1024) # Receive data from client
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Received message from {controller_address}: {data}")
  
    try:
      control_data = json.loads(data.decode('utf-8')) # Decode the JSON object
      print("Decoded control data as JSON object:", control_data)
    except json.JSONDecodeError as e:
      print("Failed to decode control data as JSON object:", e)

    # Checking that the UDP packet was correctly transmitted
    expected_keys = {"js_x", "js_y", "left", "right", "fire"}
    if not expected_keys.issubset(control_data.keys()):
      print("Missing one or more expected keys in control data")
      continue
    
    # DC Motor Control #
    # Motor speeds are between -100 and 100
    base_speed = round(100 * ((control_data["js_y"] - CONTROLLER_ADC_MAX/2) / (CONTROLLER_ADC_MAX / 2))) # -100 to 100
    turn_adjust = round(100 * ((control_data["js_x"] - CONTROLLER_ADC_MAX/2) / (CONTROLLER_ADC_MAX / 2))) # -100 to 100
    
    left_speed = max(-100, min(base_speed - turn_adjust, 100)) # Clamps speed between -100 and 100
    right_speed = max(-100, min(base_speed + turn_adjust, 100)) # Clamps speed between -100 and 100
    
    left_motor.drive(left_speed) # drive left motor
    right_motor.drive(right_speed) # drive right motor
  
    # Servo Motor Control #
    # Servo angles (0 to 180 degrees) are mapped to values (-1 to 1)
    if control_data["left"] != control_data["right"]:
      if control_data["left"] == 1:
        servo.left()
      if control_data["right"] == 1:
        servo.right()
    else:
      servo.stop()

    # FIRE! #
    if control_data["fire"] == 1:
      # Do fire logic
except KeyboardInterrupt:
  print("\nShutting down tank controls...")
  left_motor.standby(True)
  right_motor.standby(True)
  servo.stop()
  tank_socket.close()
    
