from temp_sensor_interface_V2 import SensorType, SensorReader


sensor_reader = SensorReader()

temperature = sensor_reader.read_value(SensorType.TEMPERATURE)
print(f"Temperature: {temperature}°C")

humidity = sensor_reader.read_value(SensorType.HUMIDITY)
print(f"Humidity: {humidity}%")

