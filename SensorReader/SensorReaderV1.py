import serial
import time
import struct
import threading

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

def add_crc(str_command):
    bytes_send = bytes([int(x, 16) for x in str_command]) # list to bytes
    crc = modbusCRC(bytes_send) # CRC calculator function
    str_command.append(str('{:02X}'.format(crc[0]))) # append crc LO 
    str_command.append(str('{:02X}'.format(crc[1]))) # append crc HI   
    return str_command 

def modbus_send(ser, str_command):
    bytes_send = bytes([int(x, 16) for x in str_command])
    ser.write(bytes_send) # send command

def hex_to_float(hex_string):
    byte_sequence = bytes.fromhex(hex_string)
    float_value = struct.unpack('>f', byte_sequence)[0]
    
    return float_value
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
    ['01', '03', '16', '31', '00', '07', '51', '8F'],
    ['01', '03', '16', '38', '00', '07', '81', '8D'],
    ['01', '03', '16', '3F', '00', '07', '30', '4C'],
    ['01', '03', '16', '46', '00', '07', 'E1', '95'],
    ['01', '03', '16', '4D', '00', '07', '90', '57'],
    ['01', '03', '16', '54', '00', '07', '41', '90'],
    ['01', '03', '16', '5B', '00', '07', '71', '93'],
    ['01', '03', '16', '62', '00', '07', 'A1', '9E'],
    ['01', '03', '16', '69', '00', '07', 'D0', '5C'],
    ['01', '03', '16', '93', '00', '07', 'F0', '6D'],
    ['01', '03', '16', '9A', '00', '07', '20', '6F'],
    ['01', '03', '16', 'A1', '00', '07', '51', 'A2'],
    ['01', '03', '16', 'A8', '00', '07', '81', 'A0'],
    ['01', '03', '16', 'BD', '00', '07', '90', '64'],
    ['01', '03', '16', 'C4', '00', '07', '41', 'BD'],
    ['01', '03', '16', 'D9', '00', '07', 'D1', 'BB'],
    ['01', '03', '16', 'E0', '00', '07', '01', 'B6'],
    ['01', '03', '17', '18', '00', '07', '81', 'BB'],
    ['01', '03', '17', '1F', '00', '07', '30', '7A'],
    ['01', '03', '17', '26', '00', '07', 'E0', '77'],
    ['01', '03', '17', '2D', '00', '07', '91', 'B5'],
    ['01', '03', '17', '73', '00', '07', 'F0', '67'],
    ['01', '03', '17', '7A', '00', '07', '20', '65'],
    ['01', '03', '17', 'A4', '00', '07', '40', '5F']
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
    "rhodamine_wt_concentration",
    "rhodamine_wt_fluorescence_intensity",
    "chloride_mv",
    "nitrate_as_nitrogen_concentration",
    "nitrate_mv",
    "ammonium_as_nitrogen_concentration",
    "ammonium_mv",
    "ammonia_as_nitrogen_concentration",
    "total_ammonia_as_nitrogen_concentration",
    "eh",
    "velocity",
    "chlorophyll_a_concentration",
    "chlorophyll_a_fluorescence_intensity",
    "blue_green_algae_phycocyanin_concentration",
    "blue_green_algae_phycocyanin_fluorescence_intensity",
    "blue_green_algae_phycoerythrin_concentration",
    "blue_green_algae_phycoerythrin_fluorescence_intensity",
    "fluorescein_wt_concentration",
    "fluorescein_wt_fluorescence_intensity",
    "fluorescent_dissolved_organic_matter_concentration",
    "fluorescent_dissolved_organic_matter_fluorescence_intensity",
    "crude_oil_concentration",
    "crude_oil_fluorescence_intensity",
    "colored_dissolved_organic_matter_concentration"
]
def main():
    ser = "" 
    while(True):    
        try:
            if(ser == ""): 
                ser = serial.Serial(port = 'COM9', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1, timeout = 2) # define COM PORT and baudrateser = serial.Serial(port = 'COM9', baudrate = 19200, bytesize = 8, parity = 'E', stopbits = 1, timeout = 3) # define COM PORT and baudrate
            command_wake_up = ["01", "0D"] 
            command_wake_up = add_crc(command_wake_up)
            print("Request: ", command_wake_up)
            modbus_send(ser, command_wake_up)
            time.sleep(0.2)
            modbus_send(ser, command_wake_up)
            data = ser.read(5)
            data = [format(x, '02x') for x in data]
            print("Response :", data)
            
            for i in range(len(command_set)):
                print(f"idx: {i+1} Request: ", command_set[i])
                modbus_send(ser = ser, str_command = command_set[i])
                time.sleep(1)
                data = ser.read(19)
                data = [format(x, '02x') for x in data]
                print("Response :", data)
                if(len(data) == 19):
                    device_id = data[0]
                    function_code = data[1]
                    measured_value = hex_to_float(data[3] + data[4] + data[5] + data[6])
                    data_quality = int((data[7] + data[8]), 16)
                    print("device_id: ", device_id)
                    print("function_code: ", function_code)
                    print(f"measured_value({parameter_names[i]}): ", measured_value)
                    if data_quality == 0:
                        print("No errors or warnings.")
                    elif data_quality == 3:
                        print("Error reading parameter.")
                    elif data_quality == 5:
                        print("RDO Cap expired.")

                print()

        except serial.serialutil.SerialException:
            ser = "" 
            print("Serial Error...")
            print("Trying to reconnect...")
            time.sleep(3)
            continue

        except Exception as e:
            print(e)

        time.sleep(10)

main_thread = threading.Thread(target = main)  # define thread
main_thread.start() # thread start

