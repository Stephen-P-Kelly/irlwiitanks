import motor_driver
import servo_driver
from time import sleep

# Motor Driver
AIN1 = 14
AIN2 = 15
PWMA = 18
BIN1 = 17
BIN2 = 27
PWMB = 22
STBY = 23
# Servo
PWM = 24

print("Initializing motors...")
# DC
left_motor = DCMotor(AIN1, AIN2, PWMA, STBY, False)
right_motor = DCMotor(BIN1, BIN2, PWMB, STBY, False)
left_motor.standby(True)
right_motor.standby(True)
# Servo
servo = Servo(PWM)
# servo = Servo(PWM, initial_value=0) # Sucks because it's software PWM

print("Testing DC motors...")
for i in range(11): # ramp speed
  print("Speed " + i*10)
  left_motor.drive(i*10)
  right_motor.drive(i*10)
  sleep(0.5)
left_motor.brake()
right_motor.brake()
sleep(2)
left_motor.drive(50) # spin CW
right_motor.drive(-50)
sleep(2)
left_motor.brake()
right_motor.brake()
sleep(2)
left_motor.drive(-50) # spin CCW
right_motor.drive(50)
sleep(2)
left_motor.brake()
right_motor.brake()
sleep(1)
left_motor.standby(True) # standby
right_motor.standby(True)
print("Done testing motors! :)")
sleep(3)

print("Testing servo...")
servo.set_angle(0)
sleep(1)
servo.set_angle(90)
sleep(1)
servo.set_angle(180)
sleep(1)
servo.set_angle(0)
sleep(2)
for i in range(90): # Going right
  servo.right()
  sleep(0.04)
sleep(1)
for i in range(90): # Going left
  servo.left()
  sleep(0.04)
sleep(1)
servo.smooth_dance() # dance :)
print("Done testing servo!")


