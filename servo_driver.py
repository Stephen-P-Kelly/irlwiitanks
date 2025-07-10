# Servo motor driver
import pigpio
from random import random
import time

''' 
Converts the degrees for the servo to PWM input.
It is unsafe for the servo to go below 500 us duty cycle or above
2500 us duty cycle. This function keeps the servo within those bounds.
  0 deg   -->  510 us
  90 deg  -->  1500 us
  180 deg -->  2490 us
'''
deg2pwm = lambda deg: 510 + 11*deg


'''
Purpose:
  This class is made to control the SG90 servo motors
Info:
  Servo motor angles are to be given as numbers between 0 and 180 (degrees)
'''
class Servo:
  pwm = ""
	pwm_pin = ""
	angle = ""

	#Defaults
	hertz = 50 # Hz
  duty = 1000 # us

	#Constructor
	def __init__(self, pwm_pin, init_angle=90):
    '''
    Param:
      pwm_pin - The GPIO pin for the PWM signal
      init_angle - Initial angle for the servo
    '''
		self.pwm_pin = pwm_pin
    self.ang = init_angle

    self.pwm = pigpio.pi()
    self.pwm.set_mode(pwm_pin, pigpio.OUTPUT)
    self.pwm.set_PWM_frequency(pwm_pin, 50)
    self.pwm.set_servo_pulsewidth(pwm_pin, deg2pwm(self.ang))

	def angle(self, degree):
    if degree >= 0 and degree <= 180:
      self.ang = degree
  		self.pwm.set_servo_pulsewidth(pwm_pin, deg2pwm(self.ang))
    else:
      print("Servo is at max angle of " + str(self.ang) + "!")

	def stop(self):
		self.pwm.set_servo_pulsewidth(pwm_pin, 0)
    
	def reset(self):
		self.pwm.set_servo_pulsewidth(pwm_pin, 510)

	def dance(self):
	  i = 0
    while i < 10:
      self.pwm.set_servo_pulsewidth(pwm_pin, deg2pwm(180*random()))
      time.sleep(0.5)
      i += 1

  def __del__(self):
    self.pwm.stop()
