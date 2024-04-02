#include <BluetoothSerial.h> 
BluetoothSerial SerialBT; 

char s;
int pump = 27;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("PumpControl");
  pinMode(pump, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    SerialBT.println(Serial.read());
  }
  if (SerialBT.available()) {
    s = SerialBT.read();
    if(s == '1'){
      Serial.println("open");
      SerialBT.println("open");
      digitalWrite(pump, HIGH);
    }else if(s == '0'){
      Serial.println("close");
      SerialBT.println("close");
      digitalWrite(pump, LOW);
    }else{
      Serial.println("keyin error");
      SerialBT.println("keyin error");
    }
  }
  delay(50);
}