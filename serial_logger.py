import csv
import serial

PORT = "COM5"
BAUD = 115200
OUTPUT_FILE = "sound_log.csv"

with serial.Serial(PORT, BAUD, timeout=1) as ser, open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    header_written = False

    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        print(line)

        if line == "LOGGING_COMPLETE":
            print(f"Saved to {OUTPUT_FILE}")
            break

        if line == "timestamp,rms":
            if not header_written:
                writer.writerow(["timestamp", "rms"])
                header_written = True
            continue

        if "," in line:
            parts = line.split(",", 1)
            if len(parts) == 2:
                writer.writerow(parts)