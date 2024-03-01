from temp_sensor_interface_V2 import SensorType, SensorReader
import struct
import keyboard

sensor_reader = SensorReader()

while(True):
    v = sensor_reader.read_value(SensorType.HUMIDITY)
    v = struct.unpack(">If", v)
    print(f"v: {v}%")
    
    if keyboard.is_pressed('esc'):
        break

