# 📡 Sensor Integration & Data Logging System

## 📌 Overview

This project implements a **multi-sensor data collection system** using an Arduino and a Python script. It captures real-time data from multiple sensors and logs it into a CSV file for further analysis.

---

## 🚀 Features

* 🌡️ Temperature sensor data collection
* ❤️ Pulse sensor (IR/Red) monitoring
* 🎤 Microphone/audio signal capture
* 🔌 Serial communication between Arduino and Python
* 📄 Automatic CSV data logging

---

## 🛠️ Tech Stack

* **Arduino (C/C++)** – Sensor data acquisition
* **Python** – Serial communication & data logging
* **CSV** – Data storage format

---

## 📂 Project Structure

```
Contact_Validation/
│── arduino/
│   └── sensor_reader.ino
│── python/
│   └── serial_logger.py
│── data/
│   ├── data_raw.csv
│   └── data_with_timestamps.csv 
│── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Arduino Setup

* Connect sensors:

  * Temperature sensor
  * Pulse sensor
  * Microphone module
* Upload the Arduino sketch:

  ```bash
  sensor_reader.ino
  ```

---

### 2️⃣ Python Setup

Install required dependencies:

```bash
pip install pyserial pandas
```

---

### 3️⃣ Run the Logger

```bash
python serial_logger.py
```

* Ensure the correct **COM port** is set in the script
* Data will be saved automatically to `data_raw.csv (or data_with_timestamps.csv)`

---





This project is open-source and available under the MIT License.
