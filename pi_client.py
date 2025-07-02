import paho.mqtt.client as mqtt
import time

# CHANGE THIS FOR EACH PI (e.g., "pi1", "pi2", etc.)
PI_ID = "pi1"

# Replace with your PC's IP
BROKER = "localhost"
COMMAND_TOPIC = f"commands/{PI_ID}"
RESPONSE_TOPIC = f"responses/{PI_ID}"

lives = 3

def on_connect(client, userdata, flags, rc):
    print(f"[{PI_ID.upper()}] Connected to broker.")
    client.subscribe(COMMAND_TOPIC)
    client.subscribe("commands/all")

def on_message(client, userdata, msg):
    global lives
    #command = "pi# says: 'command'""
    command = msg.payload.decode()
    print(f"[{PI_ID.upper()}] Received command: {command}")
    response = f"{PI_ID} received: {command}"
    client.publish(RESPONSE_TOPIC, response)
    #SimpleCommand = 'command'
    SimpleCommand = command.split("says:", 1)[1].strip()
    handler = command_handlers.get(SimpleCommand)
    if handler:
        handler()
    else:
        print(f"[{PI_ID.upper()}] Unknown command: {SimpleCommand}")

def start_message():
    print(f"[{PI_ID.upper()}] Game starting in...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  GO!\n")

def hit_message():
    global lives
    if lives > 0:
        lives -= 1
        print(f"[{PI_ID.upper()}] HIT! Lives remaining: {lives}")
        if lives == 0:
            print(f"[{PI_ID.upper()}] DESTROYED!")
    else:
        print(f"[{PI_ID.upper()}] Already destroyed.")

def reset_message():
    global lives
    lives = 3
    print(f"[{PI_ID.upper()}] Lives reset to {lives}.")

#Add all commands here
command_handlers = {
    "start": start_message,
    "hit": hit_message,
    "reset": reset_message
}

client = mqtt.Client(client_id=PI_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883)
client.loop_start()

try:
    while True:
        # Send a heartbeat when connecting for testing
        client.publish(RESPONSE_TOPIC, f"{PI_ID} is alive")

        # This will have to change, jsut type in terminal for now
        target = input(f"[{PI_ID.upper()}] Send to (e.g. pi2 or server): ").strip().lower()
        message = input(f"[{PI_ID.upper()}] Message to send: ").strip()
        if target and message:
            topic = f"commands/{target}"
            client.publish(topic, f"{PI_ID} says: {message}")
except KeyboardInterrupt:
    print(f"[{PI_ID.upper()}] Shutting down.")
    client.loop_stop()
    client.disconnect()

