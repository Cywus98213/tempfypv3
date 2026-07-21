import bluetooth
import struct
import time
from picamera2 import Picamera2
import cv2

phone_mac = "F0:05:1B:5A:7C:5C"
uuid = "00001101-0000-1000-8000-00805F9B34FB"

def wait_for_connection():
    while True:
        print("Waiting for Bluetooth service...")
        services = bluetooth.find_service(uuid=uuid, address=phone_mac)
        if not services:
            time.sleep(2)
            continue

        port = services[0]["port"]
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            sock.connect((phone_mac, port))
            print(f"Connected on port {port}")
            return sock
        except Exception as e:
            print(f"Connection failed: {e}")
            sock.close()
            time.sleep(2)

def stream_frames(sock):
    picam = Picamera2()
    picam.configure(picam.create_video_configuration(main={"size": (640, 480)}))
    picam.start()

    try:
        while True:
            frame = picam.capture_array()
            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            data = buffer.tobytes()

            sock.send(struct.pack(">I", len(data)))
            sock.send(data)
            print(f"Frame sent ({len(data)} bytes)")
            time.sleep(0.5)
    except Exception as e:
        print(f"Streaming stopped: {e}")
    finally:
        picam.stop()
        sock.close()

if __name__ == "__main__":
    while True:
        sock = wait_for_connection()
        stream_frames(sock)
        print("Connection closed, returning to wait mode...")
