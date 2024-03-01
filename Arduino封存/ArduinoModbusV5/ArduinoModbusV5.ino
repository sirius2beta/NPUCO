#include <SoftwareSerial.h>

byte request[] = {0x01, 0x03, 0x15, 0x4A, 0x00, 0x03, 0x20, 0x11};

void setup() {
  Serial.begin(19200, SERIAL_8E1);      // 主要的硬體串列通信，與感測器通訊
  Serial1.begin(19200, SERIAL_8E1);     // 軟體串列通信，與電腦通訊, D7, D8
}

void loop() {
  Serial.write(request, sizeof(request));
  delay(1000);
  // 與感測器通訊
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      byte dataByte = Serial.read();

      Serial1.print(dataByte, HEX);
      Serial1.print(" ");
    }
    Serial1.println();
  }
  delay(3000);
}
