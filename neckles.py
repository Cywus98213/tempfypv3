import bluetooth
import struct
import time
import cv2

phone_mac = "F0:05:1B:5A:7C:5C"
uuid = "00001101-0000-1000-8000-00805F9B34FB"

def send_all(sock, data):
    """Ensure the entire buffer is sent over Bluetooth."""
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

def wait_for_connection():
    """Keep trying until the phone app is discoverable and listening."""
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
    """Capture frames from USB webcam and stream them over Bluetooth."""
    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Failed to open /dev/video0")
        sock.close()
        return

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
            send_all(sock, data)

            print(f"Frame sent ({len(data)} bytes)")
            time.sleep(0.5)
    except Exception as e:
        print(f"Streaming stopped: {e}")
    finally:
        cap.release()
        sock.close()

if __name__ == "__main__":
    while True:
        sock = wait_for_connection()
        stream_frames(sock)
        print("Connection closed, returning to wait mode...")
