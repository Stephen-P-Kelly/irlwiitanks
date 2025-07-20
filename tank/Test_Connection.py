import socket
import json

# ──────── Network Setup ────────
UDP_IP = "10.0.0.18"
UDP_PORT = 4210

# ──────── Socket Setup ────────
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}...")

# ──────── Main Loop ────────
while True:
    data, addr = sock.recvfrom(1024)  # buffer size
    try:
        control_data = json.loads(data.decode('utf-8'))
        print("Received control data:")
        for key, value in control_data.items():
            print(f"  {key}: {value}")
    except json.JSONDecodeError:
        print("Received non-JSON data:", data)
