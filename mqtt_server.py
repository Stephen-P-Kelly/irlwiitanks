import paho.mqtt.client as mqtt

BROKER = "localhost"
PI_COMMAND_TOPIC = "commands/pi1"
PI_RESPONSE_TOPIC = "responses/pi1"

def on_connect(client, userdata, flags, rc):
    print(f"[SERVER] Connected with result code {rc}")
    client.subscribe(PI_RESPONSE_TOPIC)

def on_message(client, userdata, msg):
    print(f"[SERVER] Received from Pi: {msg.payload.decode()}")

client = mqtt.Client(client_id="Server")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883)
client.loop_start()

try:
    print("[SERVER] Type commands to send to the Pi. Type 'exit' to quit.")
    while True:
        command = input(">> ")
        if command.lower() == "exit":
            break
        client.publish(PI_COMMAND_TOPIC, command)
except KeyboardInterrupt:
    print("\n[SERVER] Exiting...")

client.loop_stop()
client.disconnect()
