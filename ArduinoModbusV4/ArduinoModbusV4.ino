#include <ModbusMaster.h>
#include <SoftwareSerial.h>

// 建立ModbusMaster物件
ModbusMaster node;

void setup() {
  // 啟用Serial通訊口，用於除錯信息
  Serial.begin(19200, SERIAL_8E1);

  // 初始化ModbusMaster物件，設定通訊串口
  node.begin(1, Serial); // 設定Slave地址為1，串口為Serial
}
void loop() {
  uint8_t result;
  uint16_t data;
  
  // 讀取保持寄存器(功能碼03)，從保持寄存器地址0讀取一個16位整數
  result = node.readHoldingRegisters(0x154A, 0x0002);
  delay(1000);
  // 檢查通訊結果
  if (result == node.ku8MBSuccess) {
    // 讀取成功，獲得數據
    data = node.getResponseBuffer(0);
    Serial.print("Read success! Data: ");
    Serial.println(data);
  } else {
    // 讀取失敗，輸出錯誤信息
    Serial.print("Read failed! Result: ");
    Serial.println(result);
  }
  delay(1000); // 每秒讀取一次
}
