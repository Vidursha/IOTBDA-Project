# Serial Logger (Python)

## 📌 Overview

This script reads data from the ESP32 via Serial (COM port) and automatically saves it into a CSV file.

---

## ⚙️ Requirements

* Python installed
* `pyserial` library

Install:

```
python -m pip install pyserial
```

---

## ▶️ How to Run

1. Close Arduino Serial Monitor
2. Open Command Prompt in the folder containing `serial_logger.py`
3. Run:

```
python serial_logger.py
```

---

## 🔌 Configuration

Edit these if needed:

```
PORT = "COM5"        # Your ESP32 port
BAUD = 115200        # Must match Arduino code
OUTPUT_FILE = "sound_log.csv"
```

---

## 📊 Output

* Reads:

```
timestamp,rms
```

* Saves automatically as:

```
sound_log.csv
```

---

## ⏹️ Stop Condition

Script stops when ESP32 sends:

```
LOGGING_COMPLETE
```

---

## ⚠️ Notes

* Only one program can use COM port → keep Serial Monitor closed
* Ensure ESP32 is running before starting script

---
