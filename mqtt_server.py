import paho.mqtt.client as mqtt

BROKER = "localhost"
RESPONSE_TOPIC = "responses/#"  # Subscribe to all Pi responses

client = mqtt.Client(client_id="Server")

def on_connect(client, userdata, flags, rc):
    print(f"[SERVER] Connected with result code {rc}")
    client.subscribe(RESPONSE_TOPIC)

def on_message(client, userdata, msg):
    print(f"[SERVER] Received on {msg.topic}: {msg.payload.decode()}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883)
client.loop_start()

try:
    print("[SERVER] Type messages in the format: pi# message")
    print("[SERVER] Or use 'all message' to send to all Pis")
    while True:
        entry = input(">> ").strip()
        if not entry:
            continue
        if entry.lower() == "exit":
            break
        try:
            target, message = entry.split(maxsplit=1)
            target = target.lower()

            # Handle broadcast
            if target in ("all"):
                topic = "commands/all"
            else:
                topic = f"commands/{target}"

            client.publish(topic, f"server says: {message}")
            print(f"[SERVER] Sent to {topic}: {message}")
        except ValueError:
            print("Format error. Use: pi1 Hello OR all Hello everyone")
except KeyboardInterrupt:
    print("\n[SERVER] Exiting...")

client.loop_stop()
client.disconnect()
