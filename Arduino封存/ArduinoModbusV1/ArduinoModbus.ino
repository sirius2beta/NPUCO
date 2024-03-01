#include <ModbusMaster.h>

#define baudrate 19200
#define timeout 1000

ModbusMaster node;

void setup() {
  Serial.begin(baudrate);

  node.begin(1, Serial); 
  node.setTimeOut(timeout);
  node.setBaudRate(baudrate);
  node.setTransmitMode();
  node.setParity(EVEN);
  node.setStopBits(1); 
  node.setDataBits(8);
}

void loop() {
  uint8_t result;
  uint8_t customRequest[] = {0x0D, 0xC1, 0xE5, 0x01};

  result = node.sendTxBuffer(customRequest, sizeof(customRequest));

  if (result == node.ku8MBSuccess) {
    Serial.println("Custom request sent successfully");

    delay(100);

    result = node.readResponseBuffer(5);

    if (result == node.ku8MBSuccess) {
      Serial.print("Response data: ");
      for (int i = 0; i < 5; i++) {
        Serial.print(node.getResponseBuffer(i), HEX);
        Serial.print(" ");
      }
      Serial.println();
    } else {
      Serial.print("Error reading response data. Error code: ");
      Serial.println(result);
    }
  } else {
    Serial.print("Error sending custom request. Error code: ");
    Serial.println(result);
  }

  delay(5000); 
}
