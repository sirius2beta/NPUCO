from enum import Enum
import serial
import time

class SensorType(Enum):
    WAKE_UP = 0
    TEMPERATURE = 1
    PRESSURE = 2
    DEPTH = 3
    LEVEL_DEPTH_TO_WATER = 4
    LEVEL_SURFACE_ELEVATION = 5
    ACTUAL_CONDUCTIVITY = 6
    SPECIFIC_CONDUCTIVITY = 7
    RESISTIVITY = 8
    SALINITY = 9
    TOTAL_DISSOLVED_SOLIDS = 10
    DENSITY_OF_WATER = 11
    BAROMETRIC_PRESSURE = 12
    PH = 13
    PH_MV = 14
    ORP = 15
    DISSOLVED_OXYGEN_CONCENTRATION = 16
    DISSOLVED_OXYGEN_SATURATION = 17
    OXYGEN_PARTIAL_PRESSURE = 20
    EXTERNAL_VOLTAGE = 22
    BATTERY_CAPACITY_REMAINING = 23

class SensorReader:
    command_set = [
        ["01", "0D", "C1", "E5"]
        ['01', '03', '15', '4A', '00', '07', '21', 'D2'],
        ['01', '03', '15', '51', '00', '07', '51', 'D5'],
        ['01', '03', '15', '58', '00', '07', '81', 'D7'],
        ['01', '03', '15', '5F', '00', '07', '30', '16'],
        ['01', '03', '15', '66', '00', '07', 'E0', '1B'],
        ['01', '03', '15', '82', '00', '07', 'A0', '2C'],
        ['01', '03', '15', '89', '00', '07', 'D1', 'EE'],
        ['01', '03', '15', '90', '00', '07', '00', '29'],
        ['01', '03', '15', '97', '00', '07', 'B1', 'E8'],
        ['01', '03', '15', '9E', '00', '07', '61', 'EA'],
        ['01', '03', '15', 'A5', '00', '07', '10', '27'],
        ['01', '03', '15', 'B3', '00', '07', 'F1', 'E3'],
        ['01', '03', '15', 'BA', '00', '07', '21', 'E1'],
        ['01', '03', '15', 'C1', '00', '07', '51', 'F8'],
        ['01', '03', '15', 'C8', '00', '07', '81', 'FA'],
        ['01', '03', '15', 'CF', '00', '07', '30', '3B'],
        ['01', '03', '15', 'D6', '00', '07', 'E1', 'FC'],
        ['01', '03', '15', 'EB', '00', '07', '70', '30'],
        ['01', '03', '15', 'F2', '00', '07', 'A1', 'F7'],
        ['01', '03', '16', '15', '00', '07', '11', '84'],
        ['01', '03', '16', '1C', '00', '07', 'C1', '86'],
        ['01', '03', '16', '23', '00', '07', 'F1', '8A'],
        ['01', '03', '16', '2A', '00', '07', '21', '88'],
        ['01', '03', '16', '31', '00', '07', '51', '8F']
    ]

    def __init__(self, port):
        self.ser = serial.Serial(port = port, baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1, timeout = 2)


    def read_value(self, sensor_type: SensorType):
        if sensor_type == SensorType.TEMPERATURE:
            bytes_send = bytes([int(x, 16) for x in self.command_set[1]])
            self.ser.write(bytes_send) # send command
            time.sleep(1)
            data = self.ser.read(19)
            data = [format(x, '02x') for x in data]
            print("Response :", data)
            return data
        elif sensor_type == SensorType.PRESSURE:
            return 1013.25  
        elif sensor_type == SensorType.DEPTH:
            return 45.0  
        elif sensor_type == SensorType.LEVEL_DEPTH_TO_WATER:
            return 1013.25  
        elif sensor_type == SensorType.LEVEL_SURFACE_ELEVATION:
            return 45.0  
        elif sensor_type == SensorType.ACTUAL_CONDUCTIVITY:
            return 1013.25  
        elif sensor_type == SensorType.RESISTIVITY:
            return 45.0  
        elif sensor_type == SensorType.SALINITY:
            return 1013.25  
        elif sensor_type == SensorType.TOTAL_DISSOLVED_SOLIDS:
            return 45.0  
        elif sensor_type == SensorType.DENSITY_OF_WATER:
            return 1013.25  
        elif sensor_type == SensorType.BAROMETRIC_PRESSURE:
            return 45.0  
        elif sensor_type == SensorType.PH:
            return 1013.25  
        elif sensor_type == SensorType.PH_MV:
            return 45.0  
        elif sensor_type == SensorType.ORP:
            return 1013.25  
        elif sensor_type == SensorType.DISSOLVED_OXYGEN_CONCENTRATION:
            return 45.0  
        elif sensor_type == SensorType.DISSOLVED_OXYGEN_SATURATION:
            return 1013.25  
        elif sensor_type == SensorType.OXYGEN_PARTIAL_PRESSURE:
            return 45.0  
        elif sensor_type == SensorType.EXTERNAL_VOLTAGE:
            return 1013.25  
        elif sensor_type == SensorType.BATTERY_CAPACITY_REMAINING:
            return 1013.25  
        else:
            raise ValueError("Unsupported sensor type")


    # ================Modbus function block================

