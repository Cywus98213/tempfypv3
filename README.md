# Bluetooth Camera Streamer

A lightweight Python-based project for streaming webcam frames over a Bluetooth RFCOMM connection. The project includes an installation script for Debian/Ubuntu-based systems and a Python client that captures frames from a local camera and sends them to a paired Bluetooth device.

## Overview

This project consists of two main components:

- install.sh: Installs the required Linux packages and Python dependencies.
- neckles.py: Opens a webcam, captures frames, encodes them as JPEG images, and sends them over Bluetooth to a configured target device.

The script is designed for environments where a USB webcam is available through V4L2 (typically /dev/video0) and where a Bluetooth-enabled receiver is available on the other end.

## Features

- Installs Python 3, OpenCV, NumPy, BlueZ, and related Bluetooth libraries
- Connects to a Bluetooth device using RFCOMM
- Captures frames from a USB webcam
- Encodes each frame as JPEG
- Sends each frame with a 4-byte length header for simple receiver parsing
- Automatically retries connection attempts if the Bluetooth service is unavailable

## Project Structure

```text
.
├── install.sh      # Dependency installation script
└── neckles.py      # Bluetooth camera streaming script
```

## Requirements

### Hardware

- A Linux-based machine (tested on Ubuntu/Debian-style systems)
- A USB webcam or compatible camera device
- A Bluetooth adapter or built-in Bluetooth support
- A paired Bluetooth target device that exposes the expected service UUID

### Software

The installation script installs the following dependencies:

- Python 3
- pip
- OpenCV
- NumPy
- BlueZ
- Bluetooth development libraries
- Camera and video utilities

## Installation

1. Open a terminal in the project directory.
2. Make the installer executable:

```bash
chmod +x install.sh
```

3. Run the installation script with sudo privileges:

```bash
sudo ./install.sh
```

This will update your package lists and install the required libraries.

## Configuration

Before running the script, review the settings in neckles.py.

### 1. Bluetooth target device

Edit the following values in neckles.py:

```python
phone_mac = "phone_mac"
uuid = "00001101-0000-1000-8000-00805F9B34FB"
```

Replace the MAC address with the address of the Bluetooth device you want to connect to.

### 2. Camera device

The script currently uses:

```python
cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
```

If your camera is exposed under a different device path, change it accordingly.

## Usage

Run the streaming script:

```bash
python3 neckles.py
```

### What happens at runtime

- The script continuously waits for the configured Bluetooth service.
- When the target device is available, it connects over RFCOMM.
- The webcam captures frames.
- Each frame is compressed as JPEG and transmitted to the connected device.
- If the connection drops, the script will attempt to reconnect automatically.

## How the Data Format Works

Each frame is transmitted as:

1. A 4-byte big-endian integer representing the JPEG payload length
2. The JPEG image data bytes

This simple framing allows the receiver to reconstruct each frame correctly.

## Troubleshooting

### Bluetooth connection issues

- Verify that the target device is paired and reachable.
- Confirm that the MAC address is correct.
- Check whether the required service UUID is available on the remote device.

### Camera issues

- Ensure the webcam is connected and detected by Linux.
- Check availability of the device node:

```bash
ls /dev/video*
```

- If your webcam is not available under /dev/video0, update the path in the script.

### Dependency issues

- Run the installer again if a package was missing.
- Ensure your system is up to date before installing packages.

## Notes

- The script uses a fixed delay of 0.5 seconds between frames.
- The current implementation is intended for experimentation and prototyping rather than production deployment.
- You may need to adjust the Bluetooth UUID and frame handling logic depending on the target receiver implementation.

## License

No explicit license has been provided for this project. If you intend to share or reuse it publicly, consider adding an appropriate license file.
