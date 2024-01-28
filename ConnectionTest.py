import serial
import time
import struct
# ================function block================
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

# ================function block================
ser = serial.Serial(port = 'COM9', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1) # define COM PORT and baudrate

command_wake_up = ["01", "0D"]
command_wake_up = add_crc(command_wake_up)
print("Request: ", command_wake_up)
modbus_send(ser, command_wake_up)
time.sleep(1)
modbus_send(ser, command_wake_up)
data = ser.read(5) # read 
data = [format(x, '02x') for x in data]
print("Response :", data)

command_get_temperature = ['01', '03', '15', '4A', '00', '03']
command_get_temperature = add_crc(command_get_temperature)
print("Request: ", command_get_temperature)
modbus_send(ser = ser, str_command = command_get_temperature)
time.sleep(1)
data = ser.read(11)
data = [format(x, '02x') for x in data]
print("Response :", data)
device_id = data[0]
function_code = data[1]
measured_value = hex_to_float(data[3] + data[4] + data[5] + data[6])
data_quality = int((data[7] + data[8]), 16)
print("device_id: ", device_id)
print("function_code: ", function_code)
print("measured_value(temperature): ", measured_value)
if data_quality == 0:
    print("No errors or warnings.")
elif data_quality == 3:
    print("Error reading parameter.")
elif data_quality == 5:
    print("RDO Cap expired.")


