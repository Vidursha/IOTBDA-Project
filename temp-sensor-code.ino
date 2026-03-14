#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(115200);
  while (!Serial); 
  
  // 1. Start I2C and Scan
  Wire.begin(21, 22);
  Serial.println("\n--- Starting I2C Scan ---");
  
  byte error, address;
  bool found = false;

  // We scan specifically for the MLX90614 default address: 0x5A
  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("SUCCESS: Device found at 0x");
      Serial.println(address, HEX);
      if (address == 0x5A) found = true;
    }
  }

  if (!found) {
    Serial.println("CRITICAL ERROR: MLX90614 (0x5A) not detected. Check wires!");
    while (1); // Stop here if sensor is missing
  }

  Serial.println("Scan complete. Initializing sensor...");

  // 2. Initialize the Library
  if (!mlx.begin()) {
    Serial.println("Library failed to connect to sensor!");
    while (1);
  }

  Serial.println("--- Setup Finished. Streaming Data Below ---\n");
}

void loop() {
  float ambient = mlx.readAmbientTempC();
  float object = mlx.readObjectTempC();

  // Data Validation Check
  if (isnan(ambient) || isnan(object)) {
    Serial.println("Failed to read from sensor!");
  } else {
    Serial.print("Ambient: "); Serial.print(ambient); Serial.print("°C | ");
    Serial.print("Object: "); Serial.print(object); Serial.println("°C");
  }

  delay(1000); 
}