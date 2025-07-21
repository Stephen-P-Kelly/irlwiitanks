import os
import subprocess
import time

client_script = 'tank_client.py'
camera_script = 'tank_video.py'
control_script = 'tank_control.py'

core_map = {
    mqtt_script: [0],
    udp_script: [1],
    camera_script: [2, 3]
}

def launch_script(script_path, cores):
    pid = os.fork()
    if pid == 0:  # child process gets pid 0
        os.sched_setaffinity(0, cores)
        os.execvp('python3', ['python3', script_path])

# setup
os.system("sudo pigpiod") # run Pi GPIO daemon (required for servo to work)
# another line to run the mqtt thing?? That might just be for the server

# run scripts on separate cores
launch_script(mqtt_script, core_map[mqtt_script])
time.sleep(1)
launch_script(udp_script, core_map[udp_script])
time.sleep(1)
launch_script(camera_script, core_map[camera_script])
