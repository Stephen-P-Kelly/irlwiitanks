import paho.mqtt.client as mqtt

BROKER = "your.computer.ip.address"  # Replace with your computer’s IP on the network
PI_COMMAND_TOPIC = "commands/pi1"
PI_RESPONSE_TOPIC = "responses/pi1"

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"[PI] Received command: {command}")
    response = f"Echo: {command}"
    client.publish(PI_RESPONSE_TOPIC, response)

client = mqtt.Client(client_id="Pi1")
client.on_message = on_message

client.connect(BROKER, 1883)
client.subscribe(PI_COMMAND_TOPIC)

client.loop_forever()
