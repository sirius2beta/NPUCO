import serial
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

def modbus_run(ser, origin_command, data_length):
    bytes_send = bytes([int(x, 16) for x in origin_command]) # list to bytes
    crc = modbusCRC(bytes_send) # CRC calculator function
    origin_command.append(str('{:02X}'.format(crc[0]))) # append crc LO 
    origin_command.append(str('{:02X}'.format(crc[1]))) # append crc HI     
    bytes_send = bytes([int(x, 16) for x in origin_command])

    ser.write(bytes_send) # send command
    data = ser.read(data_length) # read response

    return data
# ================Modbus function block================
ser = serial.Serial(port = 'COM8', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1) # define COM PORT and baudrate
origin_command = ['01', '0D'] # , 'C1', 'D5'
data = modbus_run(ser = ser, origin_command = origin_command, data_length = 5)

"""
origin_command = ['01', '03', '15', '4A', '00', '07', '21', 'D2']
data_length = int(origin_command[4] + origin_command[5]) * 2 + 5
data = modbus_run(ser = ser, origin_command = origin_command, data_length = data_length)
print(data)
"""
