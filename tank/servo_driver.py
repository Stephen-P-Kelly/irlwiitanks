# Servo motor driver
import pigpio
from random import random
import time
import math

MOVE_INCREMENT = 2 # deg

''' 
Converts the degrees for the servo to PWM input.
It is unsafe for the servo to go below 500 us duty cycle or above
2500 us duty cycle. This function keeps the servo within those bounds.
	0 deg   -->  510 us
	90 deg  -->  1500 us
	180 deg -->  2490 us
'''
deg2pwm = lambda ang: max(500, min(2500, 510 + 11*ang))


'''
Purpose:
	This class is made to control the SG90 servo motors
Info:
	Servo motor angles are to be given as numbers between 0 and 180 (degrees)
'''
class Servo:
	def __init__(self, pwm_pin, init_angle=0, hertz=50):
		'''
		Param:
		pwm_pin - The GPIO pin for the PWM signal
		init_angle - Initial angle for the servo
		'''
		self.pwm_pin = pwm_pin
		self.ang = init_angle

		self.pwm = pigpio.pi()
		if not self.pwm.connected:
		    raise RuntimeError("Failed to connect to pigpio daemon")
		self.pwm.set_mode(self.pwm_pin, pigpio.OUTPUT)
		self.pwm.set_PWM_frequency(self.pwm_pin, hertz)
		self.pwm.set_servo_pulsewidth(self.pwm_pin, deg2pwm(self.ang))

	def set_angle(self, ang):
		self.ang = max(0, min(180, ang))
		self.pwm.set_servo_pulsewidth(self.pwm_pin, deg2pwm(self.ang))

	def get_angle(self):
		return self.ang

	def CW(self):
	    self.set_angle(self.ang + MOVE_INCREMENT)

	right = CW

	def CCW(self):
	    self.set_angle(self.ang - MOVE_INCREMENT)

	left = CCW

	def dance(self):
		for i in range(10):
			self.pwm.set_servo_pulsewidth(self.pwm_pin, deg2pwm(180*random()))
			time.sleep(0.5)

	def smooth_dance(self, duration=2, cycles=3, amplitude=90):
	    start_time = time.time()
	    while time.time() - start_time < duration:
	        t = time.time()
	        angle = 90 + amplitude * math.sin(2 * math.pi * cycles * t / duration)
	        self.set_angle(angle)
	        time.sleep(0.02)

	def stop(self):
		self.pwm.set_servo_pulsewidth(self.pwm_pin, 0)

	def reset(self):
		self.pwm.set_servo_pulsewidth(self.pwm_pin, deg2pwm(0))

	def __del__(self):
		self.pwm.stop()
