import cv2
import bluetooth
import struct
import time

phone_mac = "F0:05:1B:5A:7C:5C"
uuid = "00001101-0000-1000-8000-00805F9B34FB"

services = bluetooth.find_service(uuid=uuid, address=phone_mac)
if not services:
    print("Service not found")
    exit()

port = services[0]["port"]
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((phone_mac, port))
print("Connected on port", port)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Capture failed")
            break

        # Encode as JPEG
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        data = buffer.tobytes()

        # Send length (4 bytes) + data
        sock.send(struct.pack(">I", len(data)))
        sock.send(data)
        print("Frame sent.")

        time.sleep(0.5)  # adjust for frame rate
except KeyboardInterrupt:
    print("Stopped by user")

cap.release()
sock.close()
