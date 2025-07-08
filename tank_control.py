# This file is for the purposes of:
# - Receiving UDP packets from the controller
# - Controlling the tank's DC and Servo motors using input from the UDP packets

###########
# Imports #
###########
from motor_driver_TB6612FNG import *
from time import sleep
import socket as s
import json

#######################
# Parameters / Config #
#######################
# Motor Driver
AIN1 = x
AIN2 = x
PWMA = x
BIN1 = x
BIN2 = x
PWMB = x
STBY = x
#Motor(IN1,IN2,PWM,STANDBY,(Reverse polarity?))
left_motor = DCMotor(AIN1, AIN2, PWMA, STBY, False)
right_motor = DCMotor(BIN1, BIN2, PWMB, STBY, False)

# Servo
PWM = x

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
  trigger firing logic
'''

# Setup UDP #
tank_socket = s.socket(s.AF_INET, s.SOCK_DGRAM) # Create UDP socket
tank_address = ('localhost', 12345) # Bind the socket to an address and port
tank_socket.bind(tank_address)
print("UDP server is up and listening...")

# Main control loop #
while True:
  data, controller_address = tank_socket.recvfrom(1024) # Receive data from client
  print(f"Received message from {controller_address}: {data}")

  try:
    control_data = json.loads(data.decode('utf-8')) # Decode the JSON object
    print("Decoded control data as JSON object:", control_data)
  except json.JSONDecodeError as e:
    print("Failed to decode control data as JSON object:", e)

  # DC Motor Control #
  

  # Servo Motor Control #
  
  
    
