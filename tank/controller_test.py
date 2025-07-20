import socket
import json
import sys
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

# Motor Driver pins
AIN1 = 14
AIN2 = 15
PWMA = 18
BIN1 = 17
BIN2 = 27
PWMB = 22
STBY = 23
# Servo
PWM = 24

# Networking
TANK_IP_ADDR         = "10.0.0.18"
TANK_RX_PORT         = 4210
CONTROLLER_IP_ADDR   = "10.0.0.50"    
HANDSHAKE_MSG        = "ground control to major tom"

def main():
    # Initialize hardware
    left_motor  = DCMotor(AIN1, AIN2, PWMA, STBY)
    right_motor = DCMotor(BIN1, BIN2, PWMB, STBY)
    left_motor.standby(True)
    right_motor.standby(True)
    servo = Servo(PWM, init_angle=90)

    # Setup UDP socket
    print("Setting up UDP socket to listen for tank commands...")
    tank_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        tank_socket.bind((TANK_IP_ADDR, TANK_RX_PORT))
    except OSError as e:
        print(f"Failed to bind UDP socket: {e}")
        sys.exit(1)

    tank_socket.settimeout(SOCKET_TIMEOUT)
    print(f"Socket bound on {TANK_IP_ADDR}:{TANK_RX_PORT} with timeout {SOCKET_TIMEOUT}s")

    # Handshake phase
#    while True:
#        print("Waiting for controller handshake...")
#        try:
#            data, addr = tank_socket.recvfrom(JSON_DOCUMENT_SIZE)
#            msg = data.decode("utf-8")
#        except socket.timeout:
#            print("No handshake packet—retrying...")
#            continue
#        except UnicodeDecodeError as e:
#            print("Corrupt handshake bytes:", e)
#            continue
#
#        print(f"Received handshake message: '{msg}' from {addr}")
#        if msg == HANDSHAKE_MSG and addr[0] == CONTROLLER_IP_ADDR:
#            print(f"Handshake OK from {addr}")
#            break
#        else:
#            print("Unexpected handshake or IP. Waiting...")
#
#    print("Entering main control loop.")
#
    # Main control loop
  # Main control loop
  while True:
    try:
      raw, addr = tank_socket.recvfrom(JSON_DOCUMENT_SIZE)
      print(f"Received packet from {addr}")
    except socket.timeout:
      print("No command received — stopping motors.")
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

    # ───── DC Motor Logic ─────
    # Convert joystick values to -100 to +100
    js_x = control_data["js_x"]
    js_y = control_data["js_y"]
    base_speed = round(100 * ((js_y - CONTROLLER_ADC_MAX/2) / (CONTROLLER_ADC_MAX/2)))
    turn_adjust = round(100 * ((js_x - CONTROLLER_ADC_MAX/2) / (CONTROLLER_ADC_MAX/2)))

    # Dead zones
    if abs(base_speed) < 5:
      base_speed = 0
    if abs(turn_adjust) < 5:
      turn_adjust = 0

    # Calculate final speeds
    left_speed = max(-MAX_WHEEL_SPEED, min(base_speed - turn_adjust, MAX_WHEEL_SPEED))
    right_speed = max(-MAX_WHEEL_SPEED, min(base_speed + turn_adjust, MAX_WHEEL_SPEED))

    print(f"Left Speed: {left_speed}, Right Speed: {right_speed}")
    left_motor.drive(left_speed)
    right_motor.drive(right_speed)

    # ───── Servo Logic ─────
    if control_data["left"] != control_data["right"]:
      if control_data["left"] == 1:
        print("Turning barrel left")
        servo.left()
      elif control_data["right"] == 1:
        print("Turning barrel right")
        servo.right()
    else:
      print("Stopping barrel")
      servo.stop()

    # ───── Fire Placeholder ─────
    if control_data["fire"] == 1:
      print("Fire button pressed")


if __name__ == "__main__":
    try:
        main()
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
