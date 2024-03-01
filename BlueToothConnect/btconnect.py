import bluetooth

target_name = "846888 PowerPack"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print(f"found target bluetooth device with address {target_address}")
else:
    print(f"could not find target bluetooth device nearby")
