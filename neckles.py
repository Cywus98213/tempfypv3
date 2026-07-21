import cv2
import bluetooth
import time

# Replace with your Android device's MAC address
SERVER_MAC = "00001101-0000-1000-8000-00805F9B34FB"

def find_device_port(mac_address):
    print(f"🔎 Searching for services on {mac_address}...")
    services = bluetooth.find_service(address=mac_address)

    if not services:
        raise Exception("No Bluetooth services found on device")

    # Pick the first RFCOMM service
    for svc in services:
        if svc["protocol"] == "RFCOMM":
            port = svc["port"]
            name = svc.get("name", "Unknown")
            print(f"Found RFCOMM service '{name}' on port {port}")
            return port

    raise Exception("No RFCOMM service found")

def connect_bluetooth(mac_address):
    port = find_device_port(mac_address)
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((mac_address, port))
    print(f"🔗 Connected to {mac_address} on port {port}")
    return sock

def capture_and_stream(sock):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Encode frame as JPEG
            _, buffer = cv2.imencode(".jpg", frame)
            data = buffer.tobytes()

            # Send length first, then data
            sock.send(str(len(data)).encode("utf-8") + b"\n")
            sock.send(data)
            print(f"Sent frame ({len(data)} bytes)")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupted, closing...")
    finally:
        cap.release()
        sock.close()

if __name__ == "__main__":
    sock = connect_bluetooth(SERVER_MAC)
    capture_and_stream(sock)
