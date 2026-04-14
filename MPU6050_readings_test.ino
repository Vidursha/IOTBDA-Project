#include <Wire.h>

#define MPU_ADDR 0x68

// Raw data registers
#define ACCEL_XOUT_H 0x3B
#define GYRO_XOUT_H  0x43
#define PWR_MGMT_1   0x6B

int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;

void writeRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(value);
  Wire.endTransmission();
}

int16_t read16Bit(uint8_t reg) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 2);

  int16_t highByte = Wire.read();
  int16_t lowByte = Wire.read();
  return (highByte << 8) | lowByte;
}

void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9);
  Wire.setClock(100000);
  delay(500);

  Serial.println("Initializing motion sensor...");

  // Wake up the sensor
  writeRegister(PWR_MGMT_1, 0x00);
  delay(100);

  Serial.println("Sensor initialized.");
  Serial.println("accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z");
}

void loop() {
  accelX = read16Bit(ACCEL_XOUT_H);
  accelY = read16Bit(ACCEL_XOUT_H + 2);
  accelZ = read16Bit(ACCEL_XOUT_H + 4);

  gyroX = read16Bit(GYRO_XOUT_H);
  gyroY = read16Bit(GYRO_XOUT_H + 2);
  gyroZ = read16Bit(GYRO_XOUT_H + 4);

  Serial.print(accelX);
  Serial.print(",");
  Serial.print(accelY);
  Serial.print(",");
  Serial.print(accelZ);
  Serial.print(",");
  Serial.print(gyroX);
  Serial.print(",");
  Serial.print(gyroY);
  Serial.print(",");
  Serial.println(gyroZ);

  delay(1000);
}