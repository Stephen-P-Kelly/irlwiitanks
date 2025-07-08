from gpiozero import DigitalOutputDevice, PWMOutputDevice

class DCMotor:
  def __init__(self, in1, in2, pwm, standby, reverse=False, hertz=1000):
    self.in1 = DigitalOutputDevice(in1)
    self.in2 = DigitalOutputDevice(in2)
    self.pwm = PWMOutputDevice(pwm, frequency=hertz)
    self.standby = DigitalOutputDevice(standby)
    self.reverse = reverse

    self.standby.on()  # Activate driver

  def drive(self, speed):
    # Clamp and normalize speed to 0-1 range for PWM
    pwm_val = abs(speed) / 100.0
    direction = speed > 0

    if self.reverse:
        direction = not direction

    if direction:
        self.in1.on()
        self.in2.off()
    else:
        self.in1.off()
        self.in2.on()

    self.pwm.value = pwm_val

  def brake(self):
    self.pwm.value = 0
    self.in1.on()
    self.in2.on()

  def standby_mode(self, enable):
    self.pwm.value = 0
    if enable:
        self.standby.on()
    else:
        self.standby.off()
