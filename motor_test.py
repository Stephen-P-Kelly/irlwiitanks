from motor_driver_TB6612FNG import *
from gpiozero import Servo
from time import sleep
from variables import *
import socket as s
import json

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

print("Initializing motors...")
left_motor = DCMotor(AIN1, AIN2, PWMA, STBY, False)
right_motor = DCMotor(BIN1, BIN2, PWMB, STBY, False)
left_motor.standby(True)
right_motor.standby(True)
servo = Servo(PWM, initial_value=0)

print("Testing DC motors...")
for i in range(11): # ramp speed
  print("Speed " + i*10)
  left_motor.drive(i*10)
  right_motor.drive(i*10)
  time.sleep(0.5)
left_motor.brake()
right_motor.brake()
time.sleep(2)
left_motor.drive(50) # spin CW
right_motor.drive(-50)
time.sleep(2)
left_motor.brake()
right_motor.brake()
time.sleep(2)
left_motor.drive(-50) # spin CCW
right_motor.drive(50)
time.sleep(2)
left_motor.brake()
right_motor.brake()
time.sleep(1)
left_motor.standby(True) # standby
right_motor.standby(True)
print("Done testing motors! :)")
time.sleep(3)

print("Testing servo...")
servo.min()
time.sleep(1)
servo.mid()
time.sleep(1)
servo.max()
time.sleep(1)
servo.min()
time.sleep(1)
while servo.value < 1:
  servo.value += SERVO_INCREMENT
  time.sleep(0.02)
time.sleep(1)
while servo.value > -1:
  servo.value -= SERVO_INCREMENT
  time.sleep(0.02)
print("Done testing servo! :)")
time.sleep(1)


