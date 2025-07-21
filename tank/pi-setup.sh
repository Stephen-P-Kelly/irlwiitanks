#!/bin/bash

echo "-=-=-=-=-=-=-=-=-=-=-"
echo "-=- Setting up Pi -=-"
echo "-=-=-=-=-=-=-=-=-=-=-"
echo "\n\n"

sudo apt update && sudo apt upgrade -y

sudo apt install -y git
sudo apt install -y python3-paho-mqtt   # MQTT client
sudo apt install -y python3-picamera2   # Camera module
sudo apt install -y python3-rpi.gpio    # Used in DC motor driver
sudo apt install -y python3-pigpio      # Used in servo motor driver

echo "\n\n"
echo "-=-=-=-=-=-=-=-=-=-=-=-"
echo "-=- Done Setting Up -=-"
echo "-=-=-=-=-=-=-=-=-=-=-=-"
