#include <ModbusMaster.h>

ModbusMaster node;
int led = 7;
int power = 4;
int send = 2;
uint8_t result;
 
void blink(int pin, int count){
  for(int i = 1 ; i <= count ; i++){
    digitalWrite(pin, HIGH);
    delay(500);
    digitalWrite(pin, LOW);
    delay(500); 
  }
}

void setup()
{
  Serial.begin(19200, SERIAL_8E1);
  node.begin(1, Serial);

  pinMode(led, OUTPUT);
  pinMode(power, OUTPUT);
  pinMode(send, OUTPUT);
  digitalWrite(led, LOW);
  digitalWrite(power, HIGH);
  digitalWrite(send, LOW);
}
 
void loop()
{
  result = node.readHoldingRegisters(0x154A, 3);
  blink(send, 2);
  delay(1000);

  if (result == node.ku8MBSuccess)
  {
    blink(led, 1);
  }
  delay(5000);
}