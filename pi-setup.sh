#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y git
sudo apt install -y python3-paho-mqtt

echo "--- Done Installing! ---"
