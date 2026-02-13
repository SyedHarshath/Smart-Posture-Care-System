#include <Wire.h>
#define MPU_ADDR 0x68
float Ax, Ay, Az, Gx, Gy, Gz;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); 
  Wire.write(0);    
  Wire.endTransmission(true);

  Serial.println("✅ MPU6050 Active!");
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);
  int16_t AcX = Wire.read() << 8 | Wire.read();
  int16_t AcY = Wire.read() << 8 | Wire.read();
  int16_t AcZ = Wire.read() << 8 | Wire.read();
  Ax = AcX / 16384.0;
  Ay = AcY / 16384.0;
  Az = AcZ / 16384.0;

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);
  int16_t GyX = Wire.read() << 8 | Wire.read();
  int16_t GyY = Wire.read() << 8 | Wire.read();
  int16_t GyZ = Wire.read() << 8 | Wire.read();
  Gx = GyX / 131.0;
  Gy = GyY / 131.0;
  Gz = GyZ / 131.0;

  Serial.print(Ax); Serial.print(",");
  Serial.print(Ay); Serial.print(",");
  Serial.print(Az); Serial.print(",");
  Serial.print(Gx); Serial.print(",");
  Serial.print(Gy); Serial.print(",");
  Serial.println(Gz);

  delay(300); 
}
