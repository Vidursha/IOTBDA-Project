#include <Wire.h>
#include "MAX30105.h"

MAX30105 particleSensor;

void setup() {
  Serial.begin(115200);
  Wire.begin(8, 9);

  Serial.println("Initializing MAX30102...");

  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30102 not found");
    while (1);
  }

  Serial.println("MAX30102 initialized!");
  Serial.println("ir,red");

  particleSensor.setup(); // default config
}

void loop() {
  long irValue = particleSensor.getIR();
long redValue = particleSensor.getRed();

Serial.print(irValue);
Serial.print(",");
Serial.println(redValue);

delay(500);
}