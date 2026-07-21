import os
import cv2
import bluetooth
import struct
import time

# Force headless mode (no framebuffer/X11)
os.environ["DISPLAY"] = ""

phone_mac = "F0:05:1B:5A:7C:5C"
uuid = "00001101-0000-1000-8000-00805F9B34FB"

# Discover service dynamically
services = bluetooth.find_service(uuid=uuid, address=phone_mac)
if not services:
    print("Service not found. Is the Android app running and discoverable?")
    exit()

port = services[0]["port"]
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((phone_mac, port))
print("Connected on port", port)

# Use default backend (avoid framebuffer hijack)
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print(" Capture failed")
            break

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

cap.release()
sock.close()
