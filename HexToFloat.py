import struct

hex_string = "40490fdb"

byte_sequence = bytes.fromhex(hex_string)

float_value = struct.unpack('>f', byte_sequence)[0]

print(float_value)
