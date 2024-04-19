#include <BluetoothSerial.h> 
BluetoothSerial SerialBT; 

char s;
int pump = 27;
int liquidSensor = 14;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("PumpControl");

  pinMode(pump, OUTPUT);
  pinMode(liquidSensor, INPUT);
}

void loop() {
  int waterLeakStatus = digitalRead(liquidSensor);
  /*
  if (Serial.available()) {
    SerialBT.println(Serial.read());
  }
  */
  // Serial.println(waterLeakStatus);
  if(waterLeakStatus == 0){
      digitalWrite(pump, LOW);
      Serial.println("warning: water leaking");
      SerialBT.println("warning: water leaking");
  }else{
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
  }
  delay(50);
}