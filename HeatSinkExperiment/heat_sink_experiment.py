import serial
import time
import threading
import matplotlib.pyplot as plt
from datetime import datetime
from openpyxl import Workbook

command_set = [
    "01 04 00 01 00 02 20 0B",
    "08 04 00 01 00 02 20 92"
]
time_data_a = []
time_data_b = []
temperature_data_a = []
temperature_data_b = []

def send(ser, command):
    byte_command = bytes.fromhex(command)
    ser.write(byte_command)
    response = ser.read(9) # readline()
    response = [format(x, '02x') for x in response]
    return response

def Reader():
    ser = "" 
    wb1 = Workbook()
    wb2 = Workbook()
    ws1 = wb1.active
    ws2 = wb2.active
    ws1.append(['Time', 'Temperature'])
    ws2.append(['Time', 'Temperature'])
    while(True):    
        try:
            if(ser == ""):
                ser = serial.Serial(port = 'COM8', baudrate = 9600, bytesize = 8, parity = 'N', stopbits = 1, timeout = 3) 
            for i in range(len(command_set)):
                print("指令:", command_set[i])
                data = send(ser = ser, command = command_set[i])
                value1 = data[3] + data[4]
                value2 = data[5] + data[6]
                temperature = int(value1, 16) / 10
                humidity = int(value2, 16) / 10
                print(f"溫度:{temperature} , 濕度:{humidity}")
                
                current_time = datetime.now().time().strftime('%H:%M:%S')
  
                if(i == 0):
                    time_data_a.append(current_time)
                    temperature_data_a.append(temperature)
                    ws1.append([current_time, temperature])
                    wb1.save('a.xlsx')
                else:
                    time_data_b.append(current_time)
                    temperature_data_b.append(temperature)
                    ws2.append([current_time, temperature])
                    wb2.save('b.xlsx')

            #time.sleep(0.5)

        except serial.serialutil.SerialException:
            ser = "" 
            print("Serial Error...")
            print("Trying to reconnect...")
            time.sleep(3)
            continue

        except Exception as e:
            print(e)

        time.sleep(1)
        # print("\n")

if __name__ == "__main__":
    reader_thread = threading.Thread(target = Reader)  # define thread
    reader_thread.start() # thread start

    plt.figure()

    while True:
        plt.title('Time vs Measurement')
        
        plt.subplot(2,1,1)
        plt.subplot(2,1,2)
        plt.plot(time_data_a, temperature_data_a, 'blue')
        plt.plot(time_data_b, temperature_data_b, 'red') 
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        
        # plt.draw()
        plt.pause(1)
        plt.clf()