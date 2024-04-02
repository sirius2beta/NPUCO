#include <SoftwareSerial.h>

byte request[] = {0x01, 0x03, 0x15, 0x4A, 0x00, 0x03, 0x20, 0x11};
int led = 7;
int power = 4;
int send = 2;

void blink(int pin, int count){
  for(int i = 1 ; i <= count ; i++){
    digitalWrite(pin, HIGH);
    delay(500);
    digitalWrite(pin, LOW);
    delay(500); 
  }
}

void setup() {
  Serial.begin(19200, SERIAL_8E1);      // 主要的硬體串列通信，與感測器通訊
  pinMode(led, OUTPUT);
  pinMode(power, OUTPUT);
  pinMode(send, OUTPUT);
  digitalWrite(led, LOW);
  digitalWrite(power, HIGH);
  digitalWrite(send, LOW);
}

void loop() {
  Serial.write(request, sizeof(request));
  blink(send, 2);
  delay(1000);
  // 與感測器通訊
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      byte dataByte = Serial.read();
      blink(led, 1);
    }
  }
  delay(2000);
}
