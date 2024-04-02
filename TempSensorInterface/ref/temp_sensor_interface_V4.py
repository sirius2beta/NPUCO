import xml.etree.ElementTree as ET
from TemperatureSensorInterface.ref.SensorDataType import SensorDataType
import serial
import time
import threading

class SensorReader:
    # consructor
    def __init__(self):
        self.temperature = 0.0 
        self.humidity = 0.0
        self.comport = "COM8" # define comport
        self.sensor_type = self.create_sensor_type_from_xml("D:/無人探測船專案資料/Code/NPUCO/TemperatureSensorInterface/SensorType.xml")
        
        send_thread = threading.Thread(target=self.send)
        send_thread.daemon = True # open deamon thread
        send_thread.start()

    def read_value(self, sensor_type):
        if sensor_type == self.sensor_type[0].getName():
            index = self.sensor_type[0].getValue()
            name = self.sensor_type[0].getName()
            type = self.sensor_type[0].getType()
            value = self.temperature
            
        elif sensor_type == self.sensor_type[1].getName():
            index = self.sensor_type[1].getValue()
            name = self.sensor_type[1].getName()
            type = self.sensor_type[1].getType()
            value = self.humidity
        else:
            raise ValueError("Unsupported sensor type")
            
        # print("value = ", value)
        data = [index, name, type, value]
        return self.packed_data(data)

    def send(self): # Thread
        ser = ""
        while(True):   
            try:
                if(ser == ""): 
                    ser = serial.Serial(self.comport, baudrate=9600, timeout=2)
                origin_send = ["01", "04", "00", "01", "00", "02", "20", "0B"]
                bytes_send = bytes([int(x, 16) for x in origin_send]) 
                ser.write(bytes_send)
                time.sleep(1)
                data = ser.read(9) 
                data = [format(x, '02x') for x in data]
                value1 = data[3] + data[4]
                value2 = data[5] + data[6]
                self.temperature = int(value1, 16) / 10
                self.humidity = int(value2, 16) / 10
            except:
                ser = ""
                # print("COM PORT ERROR Trying to reconnect.") 
                time.sleep(1)
                continue
    def setSerialPort(self, serial_port):
        self.comport = serial_port

    def packed_data(self, data):
        pass
        
        if len(data) > 256:
            pass 

        return data
    
    def create_sensor_type_from_xml(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        sdt = []
        for enum in root.findall(".//enum[@name='SENSOR_TYPE']/entry"):
            value = int(enum.get('value'))
            name = enum.get('name')
            type = enum.get('type')
            sdt.append(SensorDataType(value, name, type))
        return sdt
    

sr = SensorReader()
print(sr.read_value("TEMPERATURE"))
print(sr.read_value("HUMIDITY"))