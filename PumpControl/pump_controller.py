import serial
import threading
import time

def listener(ser):
    while(True):
        response = ser.readline().decode()
        print("回復:", response)

ser = serial.Serial(port = 'COM12', baudrate = 115200, bytesize = 8, parity = 'E', stopbits = 1)
reader_thread = threading.Thread(target = listener, args=(ser,), daemon=True)
reader_thread.start() 

command = 0
while(command != 'q'):
    command = input("輸入控制:")
    ser.write(command.encode())
    time.sleep(0.3)
    

   