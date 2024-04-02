import serial
import time
import struct
import threading
import tkinter as tk

# ================Modbus function block================
def modbusCRC(msg : str) -> int: # CRC calculator
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if(crc & 1):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    ba = crc.to_bytes(2, byteorder='little')

    return ba

def add_crc(str_command):
    bytes_send = bytes([int(x, 16) for x in str_command]) # list to bytes
    crc = modbusCRC(bytes_send) # CRC calculator function
    str_command.append(str('{:02X}'.format(crc[0]))) # append crc LO 
    str_command.append(str('{:02X}'.format(crc[1]))) # append crc HI   
    return str_command 

def modbus_send(ser, str_command):
    bytes_send = bytes([int(x, 16) for x in str_command])
    ser.write(bytes_send) # send command

def hex_to_float(hex_string):
    byte_sequence = bytes.fromhex(hex_string)
    float_value = struct.unpack('>f', byte_sequence)[0]
    
    return float_value
# ================Modbus function block================

def main():
    ser = "" 
    while(True):    
        try:
            if(ser == ""):
                ser = serial.Serial(port = 'COM10', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1, timeout = 2)
            command_wake_up = ["01", "0D", "C1", "E5"]
            print("Request: ", command_wake_up)
            modbus_send(ser, command_wake_up)
            time.sleep(1)
            modbus_send(ser, command_wake_up)
            data = ser.read(5)
            data = [format(x, '02x') for x in data]
            print("Response :", data)
            
        except serial.serialutil.SerialException:
            ser = "" 
            print("Serial Error...")
            print("Trying to reconnect...")
            time.sleep(3)
            continue

        except Exception as e:
            print(e)

        time.sleep(1)

main_thread = threading.Thread(target = main)  # define thread
main_thread.start() # thread start