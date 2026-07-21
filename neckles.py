import bluetooth
import struct
import time
from picamera2 import Picamera2
import cv2

# Replace with your phone's MAC address
phone_mac = "F0:05:1B:5A:7C:5C"
uuid = "00001101-0000-1000-8000-00805F9B34FB"

# Discover RFCOMM service
services = bluetooth.find_service(uuid=uuid, address=phone_mac)
if not services:
    print("Service not found. Is the Android app running and listening?")
    exit()

port = services[0]["port"]
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((phone_mac, port))
print(f"Connected on port {port}")

# Initialize PiCamera2 in headless mode
picam = Picamera2()
picam.configure(picam.create_video_configuration(main={"size": (640, 480)}))
picam.start()

try:
    while True:
        # Capture frame as numpy array
        frame = picam.capture_array()

        # Encode as JPEG
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        data = buffer.tobytes()

        # Send length (4 bytes) + data
        sock.send(struct.pack(">I", len(data)))
        sock.send(data)
        print(f"Frame sent ({len(data)} bytes)")

        time.sleep(0.5)  # adjust for frame rate
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    picam.stop()
    sock.close()
