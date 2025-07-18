import os
import subprocess
import time

# Define paths to your scripts
camera_script = '/home/pi/camera_stream.py'
udp_script = '/home/pi/udp_handler.py'
mqtt_script = '/home/pi/mqtt_client.py'

# Core assignments (you can change these as needed)
core_map = {
    mqtt_script: [0],
    udp_script: [1],
    camera_script: [2, 3]
}

# Function to launch a script on a specific core
def launch_script(script_path, cores):
    # Set CPU affinity for the current process
    pid = os.fork()
    if pid == 0:  # Child process
        os.sched_setaffinity(0, cores)
        os.execvp('python3', ['python3', script_path])

# Launch each script on its designated core
launch_script(mqtt_script, core_map[mqtt_script])
time.sleep(1)  # Optional: small delay between launches
launch_script(udp_script, core_map[udp_script])
time.sleep(1)
launch_script(camera_script, core_map[camera_script])
