#Raspberry Pi TB6612FNG Library
import RPi.GPIO as GPIO

#See https://raspberrypi.stackexchange.com/a/12967 for more info
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
aggression_level = {"slow": 5, "normal": 10, "fast": 20}

class DCMotor:
	#Constructor
	def __init__(self, in1, in2, pwm, standbyPin, reverse=False, hertz=1000):
		self.in1 = in1
		self.in2 = in2
		self.pwm = pwm
		self.standbyPin = standbyPin
		self.reverse = reverse
		self.speed = 0

		GPIO.setup(in1,GPIO.OUT)
		GPIO.setup(in2,GPIO.OUT)
		GPIO.setup(pwm,GPIO.OUT)
		GPIO.setup(standbyPin,GPIO.OUT)
		GPIO.output(standbyPin,GPIO.HIGH)
		self.p = GPIO.PWM(pwm, hertz)
		self.p.start(0)

	def drive(self, speed):
	    self.speed = max(-100, min(100, speed))  # Clamp between -100 and 100
		
	    if self.reverse:
	        self.speed *= -1
	
	    dutyCycle = abs(self.speed)
	
	    GPIO.output(self.in1, GPIO.HIGH if self.speed > 0 else GPIO.LOW)
	    GPIO.output(self.in2, GPIO.LOW if self.speed > 0 else GPIO.HIGH)
	    self.p.ChangeDutyCycle(dutyCycle)
	
	def ramp_drive(self, target, step=5):
		if abs(target - self.speed) < step:
			self.speed = target
		else:
			self.speed = self.speed + step if target > self.speed else self.speed - step
		self.drive(self.speed)

	def brake(self):
		self.p.ChangeDutyCycle(0)
		GPIO.output(self.in1,GPIO.HIGH)
		GPIO.output(self.in2,GPIO.HIGH)

	def standby(self, value):
		self.p.ChangeDutyCycle(0)
		GPIO.output(self.standbyPin,value)

	def __del__(self):
		GPIO.cleanup([self.in1, self.in2, self.pwm, self.standbyPin])
