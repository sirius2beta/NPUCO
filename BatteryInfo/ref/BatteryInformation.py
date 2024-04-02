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
command_set = [
    ["DD", "A5", "03", "00", "FF", "FD", "77"],
    ["DD", "A5", "04", "00", "FF", "FC", "77"]
]

def parse_basic_info(data):  
    
    function_code = data[1]
    data_length = int(data[3], 16)

    #print("function_code : ", function_code)
    #print("data_length : ", data_length)

    if(data[2] == "00"):
        total_voltage = int(data[4] + data[5], 16) / 100
        print("總電壓 : ", total_voltage, "V")

        current = int(data[6] + data[7], 16) / 100
        print("電流 : ", current, "A")

        residual_capacity = int(data[8] + data[9], 16) / 100
        print("剩餘容量 : ", residual_capacity, "A")

        nominal_capacity = int(data[10] + data[11], 16) / 100
        print("標準容量 : ", nominal_capacity, "A")

        cell_block_numbers = int(data[25], 16)
        print("電池串數 : ", cell_block_numbers)

def parse_voltage_info(data):
    function_code = data[1]
    data_length = int(data[3], 16)

    #print("function_code : ", function_code)
    #print("data_length : ", data_length)
    count = 1
    if(data[2] == "00"):
        for i in range(4 ,len(data) - 3, 2):
            vol = int(data[i] + data[i + 1], 16) / 100
            print(f"第 {count:02d} 串電壓 : {vol} V")
            count = count + 1 

def main():
    ser = "" 
    while(True):    
        try:
            if(ser == ""):
                ser = serial.Serial(port = 'COM8', baudrate = 9600, timeout = 10)
            
            # print("Request : ", command_set[0])
            modbus_send(ser = ser, str_command = command_set[0])
            basic_info = ser.read(34)
            basic_info = [format(x, '02x') for x in basic_info]
            # print("Response : ", basic_info)
            parse_basic_info(basic_info)

            # print("Request : ", command_set[1])
            modbus_send(ser = ser, str_command = command_set[1])
            voltage_info = ser.read(33)
            voltage_info = [format(x, '02x') for x in voltage_info]
            # print("Response : ", voltage_info)
            parse_voltage_info(voltage_info)

        except serial.serialutil.SerialException:
            ser = "" 
            print("Serial Error...")
            print("Trying to reconnect...")
            time.sleep(3)
            continue

        except Exception as e:
            print(e)
            time.sleep(3)
            continue
        
        print()
        time.sleep(5)

main_thread = threading.Thread(target = main)  # define thread
main_thread.start() # thread start

label = tk.Label()