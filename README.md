# 🌐 IoTBDA Project -- Sensor Integration & Hardware Setup

## 📌 Project Overview

This project is part of the **IoT and Big Data Analytics (IoTBDA)**
module.\
The goal of this project is to integrate multiple biomedical and
environmental sensors with a **microcontroller (ESP32)** and prepare the
system for data acquisition.

The sensors used in this project include:

-   **MPU6050** -- Motion tracking (Accelerometer + Gyroscope)
-   **MAX30100** -- Heart Rate & SpO₂ monitoring
-   **MLX90614** -- Infrared temperature sensor

All sensors communicate with the **ESP32 microcontroller using the I2C
protocol**.\
The team collaboratively completed the **hardware setup and wiring
stage**, ensuring that the sensors were correctly connected and ready
for data acquisition.

------------------------------------------------------------------------

# 🔧 Hardware Components

  Component      Description
  -------------- ---------------------------------------------------------
  ESP32          Microcontroller used to interface with sensors
  MPU6050        Motion sensor for acceleration and gyroscope data
  MAX30100       Sensor for heart rate and oxygen saturation
  MLX90614       Infrared sensor for non-contact temperature measurement
  Breadboard     Used to prototype the circuit
  Jumper Wires   Used for connecting sensors to ESP32

------------------------------------------------------------------------

# ⚙️ Communication Protocol

All sensors are connected using **I2C communication**, which uses two
main lines:

-   **SDA (Serial Data Line)** -- Data transmission
-   **SCL (Serial Clock Line)** -- Clock synchronization

Additional required connections: - **VCC** -- Power supply - **GND** --
Ground reference

------------------------------------------------------------------------

# 👨‍💻 Team Work Distribution (Hardware Setup & Wiring)

## 1️⃣ Dayana Priyadharshani Kumar -- IT22178640

-   Participated in the **hardware setup of the ESP32 microcontroller**
-   Assisted in wiring **MPU6050, MAX30100, and MLX90614 sensors**
-   Verified **VCC, GND, SDA, and SCL connections** for all sensors
-   Ensured sensors were **properly powered and securely connected** on
    the breadboard

------------------------------------------------------------------------

## 2️⃣ Harishalinee Elangovan -- IT22057488

-   Contributed to **ESP32 configuration and hardware preparation**
-   Assisted in connecting **MPU6050, MAX30100, and MLX90614 sensors**
-   Checked **pin connections and wiring stability**
-   Helped **identify and troubleshoot hardware connection issues**

------------------------------------------------------------------------

## 3️⃣ Vidursha Prabagaran -- IT22294098

-   Assisted in **setting up the ESP32 microcontroller environment**
-   Participated in wiring **all three sensors**
-   Verified **I2C communication lines (SDA & SCL)**
-   Organized and secured the **breadboard circuit layout**

------------------------------------------------------------------------

## 4️⃣ Kaushalya Nagenthraraja -- IT22289384

-   Participated in the **overall hardware setup and wiring**
-   Assisted in connecting **MPU6050, MAX30100, and MLX90614 sensors**
-   Verified that **all sensors were correctly powered and connected**
-   Performed **final hardware validation checks** before proceeding to
    the programming phase

------------------------------------------------------------------------

# ✅ Current Project Progress

✔ Hardware setup completed\
✔ Sensor wiring verified\
✔ I2C communication connections established

### 🚧 Next Stage

-   Sensor calibration
-   Reading sensor values programmatically
-   Handling noisy or missing values
-   Packaging sensor data into **structured JSON format**
-   Integration with IoT data processing pipeline

------------------------------------------------------------------------

# 📚 Module

**IoT and Big Data Analytics (IoTBDA)**

------------------------------------------------------------------------

# 👥 Team

-   Dayana Priyadharshani Kumar -- IT22178640
-   Harishalinee Elangovan -- IT22057488
-   Vidursha Prabagaran -- IT22294098
-   Kaushalya Nagenthraraja -- IT22289384

------------------------------------------------------------------------

⭐ *This project demonstrates the integration of IoT sensors with
microcontrollers as a foundation for real-time data analytics.*
