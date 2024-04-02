import serial
import time
import threading

# ================Modbus function block================
def modbus_send(ser, str_command):
    bytes_send = bytes([int(x, 16) for x in str_command])
    ser.write(bytes_send) # send command
# ================Modbus function block================
command_set = [
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

parameter_names = [
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
    "chloride",
    "turbidity",
    "oxygen_partial_pressure",
    "total_suspended_solids",
    "external_voltage",
    "battery_capacity_remaining",
    "rhodamine_wt_concentration"
]

def main():
    ser = "" 
    while(True):    
        try:
            if(ser == ""):
                ser = serial.Serial(port = '/dev/ttyUSB0', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1, timeout = 2)
            command_wake_up = ["01", "0D", "C1", "E5"]
            print("Request: ", command_wake_up)
            modbus_send(ser, command_wake_up)
            time.sleep(1)
            modbus_send(ser, command_wake_up)
            data = ser.read(5)
            data = [format(x, '02x') for x in data]
            print("Response: ", data)
            
            for i in range(len(command_set)):
                print(f"idx: {i+1} Request: ", command_set[i])
                modbus_send(ser = ser, str_command = command_set[i])
                time.sleep(1)
                data = ser.read(19)
                data = [format(x, '02x') for x in data] 
                print("Response: ", data)

        except serial.serialutil.SerialException:
            ser = "" 
            print("Serial Error...")
            print("Trying to reconnect...")
            time.sleep(3)
            continue

        except Exception as e:
            print(e)

        time.sleep(1)

main_thread = threading.Thread(target = main)  # define thread
main_thread.start() # thread start
