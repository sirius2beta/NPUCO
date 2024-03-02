from temp_sensor_interface_V3 import SensorReader
import struct
import keyboard
import time

sensor_reader = SensorReader()

data = sensor_reader.read_value("HUMIDITY")
data = struct.unpack("<If", data)
print("data:", data)

sensor_reader.setSerialPort("COM8")

time.sleep(10)

data = sensor_reader.read_value("HUMIDITY")
data = struct.unpack("<If", data)
print("data:", data)

