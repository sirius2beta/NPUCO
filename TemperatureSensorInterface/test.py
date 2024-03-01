import xml.etree.ElementTree as ET

file_path = "DefineData.xml"

tree = ET.parse(file_path)

root = tree.getroot()

# find "SENSOR_TYPE" entry
sensor_type = root.find(".//enum[@name='SENSOR_TYPE']")
for entry in sensor_type.findall("entry"):
    value = entry.get("value")
    name = entry.get("name")
    type = entry.get("type")
    print(f'Entry: Value={value}, Name={name}, Type={type}')
