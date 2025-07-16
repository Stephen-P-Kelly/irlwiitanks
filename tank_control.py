import sys
import socket
import json
from datetime import datetime
from motor_driver import DCMotor
from servo_driver import Servo

################
# Configuration
################
CONTROLLER_ADC_MAX   = 4096
MAX_WHEEL_SPEED      = 100
BARREL_SPEED         = 0.018   # 90°/s
BARREL_MAX_ANGLE     = 180     # degrees
JSON_DOCUMENT_SIZE   = 256     # bytes
SOCKET_TIMEOUT       = 5       # seconds

# Motor Driver pins (replace x with real GPIO numbers)
AIN1 = x
AIN2 = x
PWMA = x
BIN1 = x
BIN2 = x
PWMB = x
STBY = x

# Servo pin
PWM = x

# Networking
TANK_IP_ADDR         = "192.168.137.10"
TANK_RX_PORT         = 4210
CONTROLLER_IP_ADDR   = "192.168.137.11"
HANDSHAKE_MSG        = "ground control to major tom"


def main():
  left_motor = right_motor = servo = tank_socket = None # for safe cleanup
  try:
    # Initialize hardware
    left_motor  = DCMotor(AIN1, AIN2, PWMA, STBY)
    right_motor = DCMotor(BIN1, BIN2, PWMB, STBY)
    left_motor.standby(True)
    right_motor.standby(True)
    servo = Servo(PWM, init_angle=90)

    # Setup UDP socket
    print("Setting up UDP socket to talk to tank...")
    tank_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tank_socket.bind((TANK_IP_ADDR, TANK_RX_PORT))
    tank_socket.settimeout(SOCKET_TIMEOUT)
    print("Socket ready with a timeout of", SOCKET_TIMEOUT, "seconds.")

    # Handshake
    while True:
      print("Waiting for controller handshake...")
      try:
        data, addr = tank_socket.recvfrom(JSON_DOCUMENT_SIZE)
        msg = data.decode("utf-8")
      except socket.timeout:
        print("No handshake packet—retrying...")
        continue
      except UnicodeDecodeError as e:
        print("Corrupt handshake bytes:", e)
        continue

      if msg == HANDSHAKE_MSG and addr[0] == CONTROLLER_IP_ADDR:
        print(f"Handshake OK from {addr}")
        break
      else:
        print("Unexpected handshake:", msg)
        sys.exit(1)

    # Main control loop
    while True:
      try:
        raw, addr = tank_socket.recvfrom(JSON_DOCUMENT_SIZE)
      except socket.timeout:
        print("No command received—stopping motors.")
        left_motor.drive(0)
        right_motor.drive(0)
        continue

      # Decode JSON
      try:
        control_data = json.loads(raw.decode("utf-8"))
      except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print("Invalid JSON packet:", e)
        continue

      # Validate keys
      expected_keys = {"js_x", "js_y", "left", "right", "fire"}
      if not expected_keys.issubset(control_data):
        print("Missing keys in control data:", control_data.keys())
        continue

      # -- DC motor logic (same as before) --
      # calculate speeds
      base_speed  = round(100 * ( (control_data["js_y"] - CONTROLLER_ADC_MAX/2) / (CONTROLLER_ADC_MAX/2) ))
      turn_adjust = round(100 * ( (control_data["js_x"] - CONTROLLER_ADC_MAX/2) / (CONTROLLER_ADC_MAX/2) ))
      # dead zones
      if abs(base_speed) < 5:  base_speed = 0
      if abs(turn_adjust) < 5: turn_adjust = 0
      # calculate left and right wheel speeds
      left_speed  = max(-MAX_WHEEL_SPEED, min(base_speed - turn_adjust, MAX_WHEEL_SPEED))
      right_speed = max(-MAX_WHEEL_SPEED, min(base_speed + turn_adjust, MAX_WHEEL_SPEED))
      # drive the motors
      left_motor.drive(left_speed)
      right_motor.drive(right_speed)

      # -- Servo logic (driver clamps angle for you) --
      if control_data["left"] != control_data["right"]:
        if control_data["left"] == 1:
          servo.left()
        if control_data["right"] == 1:
          servo.right()
      else:
        servo.stop()

      # -- Fire logic placeholder --
      if control_data["fire"] == 1:
        # implement your firing sequence here
        pass
  except KeyboardInterrupt:
    print("\nKeyboardInterrupt caught. Exiting...")
    try:
      if left_motor:  left_motor.standby(True)
      if right_motor:  right_motor.standby(True)
      if servo:       servo.stop()
      if tank_socket: tank_socket.close()
    except Exception as e:
      print("Error during cleanup:", e)
    print("Cleanup complete.")


if __name__ == "__main__":
  main()
  sys.exit(0)
