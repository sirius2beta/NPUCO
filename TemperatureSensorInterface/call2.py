from temp_sensor_interface_V3 import SensorReader
import struct
import keyboard

sensor_reader = SensorReader()

while(True):
    data = sensor_reader.read_value("HUMIDITY")
    data = struct.unpack("<If", data)
    print("data:", data)

    if keyboard.is_pressed('esc'):
        break

