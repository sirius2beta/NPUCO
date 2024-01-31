#include <SoftwareSerial.h>

unsigned char item[8] = {0x01, 0x0D, 0x00, 0x00, 0x00, 0x00, 0x2C, 0x0B};
String data = "";
SoftwareSerial sensorSerial(0, 1);  // RX, TX

void setup()
{
  sensorSerial.begin(19200);
  Serial.begin(19200);
}

void loop()
{
  delay(500);
  for (int i = 0 ; i < 8 ; i++) {  // 傳送命令
    sensorSerial.write(item[i]);   // write輸出
  }
  delay(100);  // 等待測溫資料返回
  
  data = "";
  while (sensorSerial.available()) { //從串列埠中讀取資料
    unsigned char in = (unsigned char)sensorSerial.read();  // read讀取
    Serial.print(in, HEX);
    Serial.print(',');
    data += in;
    data += ',';
  }

  if (data.length() > 0) { //先輸出一下接收到的資料
    Serial.println();
    Serial.println(data);
  }else{
    Serial.println("Error");
  }
  delay(2000);
}
