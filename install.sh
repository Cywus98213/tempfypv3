#!/bin/bash
set -e

# Update package lists
sudo apt-get update

# Install Python and OpenCV
sudo apt-get install -y python3 python3-pip python3-opencv libopencv-dev python3-numpy

# Install Bluetooth stack
sudo apt-get install -y python3-bluez libbluetooth-dev bluez

# Install camera + video utilities
sudo apt-get install -y libgl1 v4l-utils

# Verify installation
echo "✅ Dependencies installed. Testing OpenCV..."
python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"
