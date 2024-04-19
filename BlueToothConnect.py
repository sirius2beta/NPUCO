import sys
import time
import bluetooth
import struct
import select

addr = "20:FA:BB:10:1E:47"
uuid = "00001101-0000-1000-8000-00805f9b34fb"
service_matches = bluetooth.find_service(uuid=uuid, address=addr)

if len(service_matches) == 0:
    print("Couldn't find the SampleServer service.")
    sys.exit(0)
else:
    print("OK")

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("Connecting to \"{}\" on {}, port {}".format(name, host, port))

# Create the client socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
sock.setblocking(0)

while True:
    ready = select.select([sock], [], [], 1.0)  # Timeout of 1 second
    print("ready :", ready)

    if ready[0]:
        # Receive data from the server
        data = sock.recv(1)
        print(f"Received data: {data}")
        if not data:
            break
    
    data = bytes([0x01, 0x0D, 0xC1, 0xE5])
    sock.send(data)

    time.sleep(1)

sock.close()