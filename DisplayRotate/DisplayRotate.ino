#include <Keyboard.h>

//https://github.com/arduino-libraries/Keyboard/blob/master/src/Keyboard.h

#include <Wire.h>
#include "Cenz_ADXL345.h"
#include "SimpleKalmanFilter.h"

#define LED_STATUS A3

#define isRangeOf(_LOWER_B, _UPPER_B, _INPUT) ((_INPUT>_LOWER_B)&&(_INPUT<_UPPER_B))

SimpleKalmanFilter kf_X = SimpleKalmanFilter(1.3, 0.1, 0.01);
SimpleKalmanFilter kf_Y = SimpleKalmanFilter(1.3, 0.1, 0.01);
SimpleKalmanFilter kf_Z = SimpleKalmanFilter(1.3, 0.1, 0.01);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_STATUS, OUTPUT);


  
  Wire.begin(); // Initiate the Wire library
  Wire_writeTo(ADXL345_ADDR, POWER_CTL, 1 << POWER_CTL_MEASURE);
  byte readFromTemp[255];
  for(int i = 0 ; i < 50; i++){
    digitalWrite(LED_STATUS, LOW);
    delay(50);
    Wire_readFrom(ADXL345_ADDR, DATAX0, 6, readFromTemp);
    kf_X.updateEstimate((int)readFromTemp[DATAX1 - DATAX0]<<8|(int)readFromTemp[DATAX0 - DATAX0]);
    kf_Y.updateEstimate((int)readFromTemp[DATAY1 - DATAX0]<<8|(int)readFromTemp[DATAY0 - DATAX0]);
    kf_Z.updateEstimate((int)readFromTemp[DATAZ1 - DATAX0]<<8|(int)readFromTemp[DATAZ0 - DATAX0]);
    digitalWrite(LED_STATUS, HIGH);
    delay(50);
    Wire_readFrom(ADXL345_ADDR, DATAX0, 6, readFromTemp);
    kf_X.updateEstimate((int)readFromTemp[DATAX1 - DATAX0]<<8|(int)readFromTemp[DATAX0 - DATAX0]);
    kf_Y.updateEstimate((int)readFromTemp[DATAY1 - DATAX0]<<8|(int)readFromTemp[DATAY0 - DATAX0]);
    kf_Z.updateEstimate((int)readFromTemp[DATAZ1 - DATAX0]<<8|(int)readFromTemp[DATAZ0 - DATAX0]);
  }
}

void loop() {
  byte readFromTemp[255];
// Wire_readFrom(ADXL345_ADDR, DEVID, 1, readFromTemp);
//  Serial.print((int)readFromTemp[0]);
//  Serial.print("\n");
  int x,y,z;
  Wire_readFrom(ADXL345_ADDR, DATAX0, 6, readFromTemp);
  x = kf_X.updateEstimate((int)readFromTemp[DATAX1 - DATAX0]<<8|(int)readFromTemp[DATAX0 - DATAX0]);
  y = kf_Y.updateEstimate((int)readFromTemp[DATAY1 - DATAX0]<<8|(int)readFromTemp[DATAY0 - DATAX0]);
  z = kf_Z.updateEstimate((int)readFromTemp[DATAZ1 - DATAX0]<<8|(int)readFromTemp[DATAZ0 - DATAX0]);
  Serial.print(x);
  Serial.print("\t");
  Serial.print(y);
  Serial.print("\t");
  Serial.print(z);
  Serial.print("\n");

  if(isRangeOf(-50,50,x)&&isRangeOf(-280,-247,y)&&isRangeOf(-50,50,z)){
            if(digitalRead(LED_STATUS) == LOW){
              runCommand("display /rotate 0");
              digitalWrite(LED_STATUS, HIGH);
              delay(1000);
              }
    }else if(isRangeOf(-50,50,x)&&isRangeOf(-50,50,y)&&isRangeOf(200,250,z)){
        if(digitalRead(LED_STATUS) == LOW){
          runCommand("display /rotate 270");
          digitalWrite(LED_STATUS, HIGH);
          delay(1000);
          }
  }else{
    digitalWrite(LED_STATUS, LOW);
    }


  delay(100);
}

void runCommand(String command){
  //  runCommand("display /rotate 180");
  //  delay(1000);
  //  runCommand("display /rotate 0");
  //
   Keyboard.begin();
   Keyboard.press(KEY_LEFT_GUI);
   Keyboard.press('r');
    Keyboard.releaseAll();
    delay(80);
    Keyboard.print(command);
    Keyboard.press(KEY_RETURN);
    Keyboard.releaseAll();
     Keyboard.end();
  
}

void Wire_writeTo(byte dev_addr, byte reg_addr, byte val){
    Wire.beginTransmission(dev_addr); // start transmission to device 
    Wire.write(reg_addr);             // send register address
    Wire.write(val);                 // send value to write
    Wire.endTransmission();         // end transmission
  }

void Wire_readFrom(byte dev_addr, byte reg_addr, byte bytes2Read, byte _buff[]){
   Wire.beginTransmission(dev_addr); // start transmission to device 
    Wire.write(reg_addr);             // sends address to read from
    Wire.endTransmission();         // end transmission
    Wire.requestFrom(dev_addr, bytes2Read);    // request 6 bytes from device
    
    int i = 0;
    while(Wire.available())         // device may send less than requested (abnormal)
    { 
        _buff[i] = Wire.read();    // receive a byte
        i++;
    }
//    if(i != num){
//        status = ADXL345_ERROR;
//        error_code = ADXL345_READ_ERROR;
//    }
  }
