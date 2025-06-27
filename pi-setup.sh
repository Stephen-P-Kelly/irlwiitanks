#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y git
sudo apt install -y python3-pip
pip3 install paho-mqtt

echo "--- Done Installing! ---"
