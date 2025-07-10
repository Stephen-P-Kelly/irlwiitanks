#Raspberry Pi TB6612FNG Library
import RPi.GPIO as GPIO

#See https://raspberrypi.stackexchange.com/a/12967 for more info
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

class DCMotor:
	#Constructor
	def __init__(self, in1, in2, pwm, standbyPin, reverse=False, hertz=1000):
		self.in1 = in1
		self.in2 = in2
		self.pwm = pwm
		self.standbyPin = standbyPin
		self.reverse = reverse

		GPIO.setup(in1,GPIO.OUT)
		GPIO.setup(in2,GPIO.OUT)
		GPIO.setup(pwm,GPIO.OUT)
		GPIO.setup(standbyPin,GPIO.OUT)
		GPIO.output(standbyPin,GPIO.HIGH)
		self.p = GPIO.PWM(pwm, hertz)
		self.p.start(0)

	def drive(self, speed):
	    speed = max(-100, min(100, speed))  # Clamp between -100 and 100
		
	    if self.reverse:
	        speed *= -1
	
	    dutyCycle = abs(speed)
	
	    GPIO.output(self.in1, GPIO.HIGH if speed > 0 else GPIO.LOW)
	    GPIO.output(self.in2, GPIO.LOW if speed > 0 else GPIO.HIGH)
	    self.p.ChangeDutyCycle(dutyCycle)

	def brake(self):
		self.p.ChangeDutyCycle(0)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.HIGH)

	def standby(self, value):
		self.p.ChangeDutyCycle(0)
		GPIO.output(self.standbyPin,value)

	def __del__(self):
		GPIO.cleanup([self.in1, self.in2, self.pwm, self.standbyPin])
