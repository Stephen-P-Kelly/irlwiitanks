#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y git
sudo apt install -y python3-paho-mqtt
sudo apt install -y python3-picamera2
sudo apt install -y python3-rpi.gpio
sudo apt install -y python3-gpiozero

echo "\n"
echo "-=-=-=-=-=-=-=-=-=-=-=-="
echo "-=- Done Installing! -=-"
echo "-=-=-=-=-=-=-=-=-=-=-=-="
