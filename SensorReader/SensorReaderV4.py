import serial
import time
import threading
import struct

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QTimer

command_set = [
    ":010D00000000F2\r\n",
    ":0103154A000796\r\n",
    ":0103155100078F\r\n",
    ":01031558000788\r\n",
    ":0103155F000781\r\n",
    ":0103156600077A\r\n",
    ":0103158200075E\r\n",
    ":01031589000757\r\n",
    ":01031590000750\r\n",
    ":01031597000749\r\n",
    ":0103159E000742\r\n",
    ":010315A500073B\r\n",
    ":010315B300072D\r\n",
    ":010315BA000726\r\n", # ph
    ":010315C100071F\r\n", # ph_mv
    ":010315C8000718\r\n", # orp
    ":010315CF000711\r\n",
    ":010315D600070A\r\n",
    ":010315F20007EE\r\n",
    ":010316150007CA\r\n",
    ":010316230007BC\r\n",
    ":0103162A0007B5\r\n"
]

parameter_names = [
    "wake_up",
    "temperature",
    "pressure",
    "depth",
    "level_depth_to_water",
    "level_surface_elevation",
    "actual_conductivity",
    "specific_conductivity",
    "resistivity",
    "salinity",
    "total_dissolved_solids",
    "density_of_water",
    "barometric_pressure",
    "pH",
    "pH_mv",
    "orp",
    "dissolved_oxygen_concentration",
    "dissolved_oxygen_percent_saturation",
    "turbidity",
    "oxygen_partial_pressure",
    "external_voltage",
    "battery_capacity_remaining"
]

parameter_chinese_names = [
    "喚醒",
    "溫度",
    "壓力",
    "深度",
    "水平面，水位深度",
    "水平面，地表高程",
    "實際導電率",
    "特定導電率",
    "電阻率",
    "鹽度",
    "總溶解固體",
    "水密度",
    "大氣壓力",
    "pH值",
    "pH毫伏",
    "氧化還原電位",
    "溶解氧濃度",
    "溶解氧飽和度%",
    "濁度",
    "氧分壓",
    "外部電壓",
    "電池剩餘容量"
]

valueDB = [0.0] * 22

def send(ser, command):
    ser.write(command.encode())
    response = ser.readline().decode()
    return response

def Reader():
    ser = "" 
    while(True):    
        try:
            if(ser == ""):
                ser = serial.Serial(port = 'COM9', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1, timeout = 5)
            for i in range(len(parameter_names)):
                start_time = time.time() * 1000
                data = send(ser = ser, command = command_set[i])
                end_time = time.time() * 1000
                if(i != 0 and i != 13 and i != 14 and i != 15):
                    # print(data)
                    print(parameter_chinese_names[i], end = ":")
                    value = struct.unpack('>f', bytes.fromhex(data[7:15]))[0]
                    valueDB[i] = value
                    elapsed_time = end_time - start_time
                    print(f" {value:.4f} \t用時: {elapsed_time:.2f} ms")

        except serial.serialutil.SerialException:
            ser = "" 
            print("Serial Error...")
            print("Trying to reconnect...")
            time.sleep(3)
            continue

        except Exception as e:
            print(e)

        time.sleep(3)
        print("\n")


class UI:
    def __init__(self):
        self.ui = QUiLoader().load("d:/無人探測船專案資料/Code/NPUCO/SensorReader/ui/SensorReaderUI.ui")
        
        reader_thread = threading.Thread(target = Reader)  # define thread
        reader_thread.start() # thread start

        self.update_sensorvalue = QTimer(self.ui)
        self.update_sensorvalue.timeout.connect(self.updateSensorValue)
        self.update_sensorvalue.start(1000)
    def updateSensorValue(self):
        self.ui.temp.setText(str(valueDB[1]))
        self.ui.pressure.setText(str(valueDB[2]))
        self.ui.dep.setText(str(valueDB[3]))
        self.ui.LDTW.setText(str(valueDB[4]))
        self.ui.LSE.setText(str(valueDB[5]))
        self.ui.AC.setText(str(valueDB[6]))
        self.ui.SC.setText(str(valueDB[7]))
        self.ui.resistivity.setText(str(valueDB[8]))
        self.ui.salinity.setText(str(valueDB[9]))
        self.ui.TDS.setText(str(valueDB[10]))
        self.ui.DOW.setText(str(valueDB[11]))
        self.ui.BP.setText(str(valueDB[12]))
        self.ui.PH.setText(str(valueDB[13]))
        self.ui.PHmV.setText(str(valueDB[14]))
        self.ui.ORP.setText(str(valueDB[15]))
        self.ui.DOC.setText(str(valueDB[16]))
        self.ui.DOS.setText(str(valueDB[17]))
        self.ui.turbidity.setText(str(valueDB[18]))
        self.ui.OPP.setText(str(valueDB[19]))
        self.ui.EV.setText(str(valueDB[20]))
        self.ui.BCR.setText(str(valueDB[21]))

app = QApplication([])
SensorReaderUI = UI()
SensorReaderUI.ui.show()
app.exec_()