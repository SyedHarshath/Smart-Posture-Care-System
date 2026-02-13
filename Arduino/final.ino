#include <Wire.h>
#define MPU_ADDR 0x68   
int buzzerPin = 8;      

long gx_offset = 0, gy_offset = 0, gz_offset = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  
  Serial.println("MPU6050 Active!");
  delay(1000);

  Serial.println("Calibrating gyro... Keep the sensor still...");
  const int samples = 500;
  for (int i = 0; i < samples; i++) {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x43);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDR, 6, true);

    int16_t GyX = Wire.read() << 8 | Wire.read();
    int16_t GyY = Wire.read() << 8 | Wire.read();
    int16_t GyZ = Wire.read() << 8 | Wire.read();

    gx_offset += GyX;
    gy_offset += GyY;
    gz_offset += GyZ;
    delay(3);
  }

  gx_offset /= samples;
  gy_offset /= samples;
  gz_offset /= samples;
  Serial.println("Gyro calibration complete!");
  delay(500);
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);
  int16_t AcX = Wire.read() << 8 | Wire.read();
  int16_t AcY = Wire.read() << 8 | Wire.read();
  int16_t AcZ = Wire.read() << 8 | Wire.read();

  float Ax = AcX / 16384.0;
  float Ay = AcY / 16384.0;
  float Az = AcZ / 16384.0;

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);
  int16_t GyX = Wire.read() << 8 | Wire.read();
  int16_t GyY = Wire.read() << 8 | Wire.read();
  int16_t GyZ = Wire.read() << 8 | Wire.read();

  GyX -= gx_offset;
  GyY -= gy_offset;
  GyZ -= gz_offset;

  float Gx = GyX / 131.0;
  float Gy = GyY / 131.0;
  float Gz = GyZ / 131.0;

  Serial.print(Ax); Serial.print(",");
  Serial.print(Ay); Serial.print(",");
  Serial.print(Az); Serial.print(",");
  Serial.print(Gx); Serial.print(",");
  Serial.print(Gy); Serial.print(",");
  Serial.println(Gz);

  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') digitalWrite(buzzerPin, HIGH);
    else if (c == '0') digitalWrite(buzzerPin, LOW);
  }

  delay(200); 
}
