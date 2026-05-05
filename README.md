# ESP32-C3 and Sensors Testing Branch

This project demonstrates the setup and testing of the **ESP32-C3 Super Mini microcontroller** and integration with the **MPU6050 (Accelerometer + Gyroscope) sensor** using I2C communication.

---

## 🔧 Hardware Used

* ESP32-C3 Super Mini
* MPU6050 Sensor Module
* Breadboard
* Jumper Wires
* USB Type-C Cable

---

## 🚀 Phase 1: ESP32-C3 Testing

### Objective

To verify that the ESP32-C3 board is working correctly and can communicate via Serial Monitor.

### Output

* Serial Monitor displayed:

```
ESP32-C3 is working
ESP32-C3 is working
...
```

### Result

✅ ESP32-C3 successfully initialized and serial communication verified.

---

## 🔌 Phase 2: MPU6050 Sensor Integration

### Objective

To interface MPU6050 with ESP32-C3 and read sensor data.

---

## 🔗 Wiring Connections

| MPU6050 Pin | ESP32-C3 Pin |
| ----------- | ------------ |
| VCC         | 3.3V         |
| GND         | GND          |
| SDA         | GPIO 8       |
| SCL         | GPIO 9       |

---

## 🔍 Step 1: I2C Scanner Test

### Purpose

To detect if the sensor is properly connected.

### Output

```
Device found at address 0x68
```

### Result

✅ MPU6050 detected successfully.

---

## ⚠️ Note on WHO_AM_I Register

* Expected value: `0x68`
* Observed value: `0x70`

This indicates:

* The sensor responds correctly on I2C
* But uses a slightly different internal ID (clone/variant)

---

## 📊 Step 2: Sensor Data Reading (Raw Registers)

### Code Approach

Instead of using libraries, raw register reading was implemented to ensure compatibility.

### Output Sample

```
Accel X: -48 | Y: -84 | Z: 16112 || Gyro X: 232 | Y: 211 | Z: -53
Accel X: -80 | Y: -68 | Z: 16176 || Gyro X: 210 | Y: 85 | Z: -102
...
```

---

## 🤔 Why Values Change Without Movement?

Sensor readings fluctuate due to:

* Environmental vibrations
* Electrical noise
* Sensor sensitivity
* Lack of filtering

This is normal behavior.

---

## 📌 Key Learnings

* ESP32-C3 USB Serial configuration (CDC enabled)
* I2C communication setup
* Sensor detection using I2C scanner
* Handling non-standard sensor responses
* Reading raw accelerometer and gyroscope data

---


## ✅ Status

✔ ESP32 Tested
✔ MPU6050 Connected
✔ Data Reading Successful

---

## 📬 Author Notes

This project is part of a step-by-step hardware integration process using ESP32-C3.

---
