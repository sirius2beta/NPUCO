class SensorDataType:
    def __init__(self, value, name, type):
        self.value = value
        self.name = name
        self.type = type

    def __str__(self):
        return f"SensorDataType(value={self.value}, name={self.name}, type={self.type})"
    
    def getValue(self):
        return self.value

    def getName(self):
        return self.name
    
    def getType(self):
        return self.type
