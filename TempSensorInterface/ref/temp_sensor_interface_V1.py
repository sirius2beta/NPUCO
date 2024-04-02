import serial
from enum import Enum
import time

class SensorType(Enum):
    TEMPERATURE = 1
    HUMIDITY = 2

class SensorReader:
    def __init__(self):
        self.ser = serial.Serial('COM8', baudrate=9600) # define COM PORT and baudrate
        
    def read_value(self, sensor_type: SensorType):
        
        if sensor_type == SensorType.TEMPERATURE:
            command = ["01","04","00","01","00","01", "60", "0A"]
            t = self.send(command)
            return t 
        elif sensor_type == SensorType.HUMIDITY:
            command = ["01","04","00","02","00","01", "90", "0A"]
            h = self.send(command)
            return h
        else:
            raise ValueError("Unsupported sensor type")

    def send(self, origin_send):
        bytes_send = bytes([int(x, 16) for x in origin_send]) # list to bytes 
        self.ser.write(bytes_send) # send command
        time.sleep(1)
        data = self.ser.read(7) # read response
        # ============= Conversion and translate =============
        data = [format(x, '02x') for x in data]
        # print(data)
        value = int(data[3] + data[4], 16) / 10

        return value