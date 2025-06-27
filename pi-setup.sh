#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y git
sudo apt install -y mosquitto mosquitto-clients

sudo systemctl enable mosquitto
sudo systemctl start mosquitto

echo "--- Done Installing! ---"
