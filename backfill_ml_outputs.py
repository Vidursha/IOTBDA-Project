import json
import pandas as pd
import joblib
from pymongo import MongoClient

# -----------------------------
# CONFIG
# -----------------------------
MONGO_URI = "mongodb+srv://dayanapriyak_db_user:Q0nXlbKhQ64tLcRz@cluster1.npcj8bx.mongodb.net/iot_project?retryWrites=true&w=majority"

DB_NAME = "iot_project"
COLLECTION_NAME = "sensor_readings"

# -----------------------------
# LOAD SAVED ARTIFACTS
# -----------------------------
scaler = joblib.load("scaler.joblib")
stress_model = joblib.load("supervised_stress_model.joblib")
anomaly_model = joblib.load("anomaly_detection_model.joblib")

with open("feature_columns.json", "r") as f:
    feature_cols = json.load(f)

print("Loaded ML artifacts successfully.")
print("Feature order:", feature_cols)

# -----------------------------
# CONNECT TO MONGODB
# -----------------------------
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("Connected to MongoDB.")

# -----------------------------
# FETCH RECORDS WITHOUT ML OUTPUTS
# -----------------------------
records = list(collection.find({
    "ml_outputs": {"$exists": False}
}))

print(f"Records found without ml_outputs: {len(records)}")

if not records:
    print("No records need backfilling.")
    exit()

# -----------------------------
# PROCESS EACH RECORD
# -----------------------------
updated_count = 0
skipped_count = 0

for record in records:
    try:
        readings = record.get("readings", {})
        features = record.get("features", {})

        row = {
            "temperature": float(readings["temperature_c"]),
            "ir": float(readings["ir_value"]),
            "red": float(readings["red_value"]),
            "sound_rms": float(readings["sound_rms"]),
            "ir_red_ratio": float(features["ir_red_ratio"]),
            "sound_peak": float(features["sound_peak"]),
            "sound_std": float(features["sound_window_std"])
        }

        feature_df = pd.DataFrame([row])

        # Ensure exact feature order used in training
        feature_df = feature_df[feature_cols]

        # Apply same scaler used during training
        scaled_features = scaler.transform(feature_df)

        # Predict stress state
        stress_state = stress_model.predict(scaled_features)[0]

        # Predict anomaly
        anomaly_label = int(anomaly_model.predict(scaled_features)[0])
        anomaly_flag = anomaly_label == -1

        # ML-based alert logic
        stress_text = str(stress_state).lower()
        ml_alert = (
            "high" in stress_text or
            "unusual" in stress_text or
            anomaly_flag
        )

        ml_outputs = {
            "stress_state": str(stress_state),
            "ml_alert": bool(ml_alert),
            "anomaly_flag": bool(anomaly_flag),
            "anomaly_label": anomaly_label,
            "model_source": "backfilled_historical"
        }

        collection.update_one(
            {"_id": record["_id"]},
            {"$set": {"ml_outputs": ml_outputs}}
        )

        updated_count += 1

    except Exception as e:
        skipped_count += 1
        print(f"Skipped record {record.get('_id')} because: {e}")

# -----------------------------
# SUMMARY
# -----------------------------
print("\nBackfill completed.")
print(f"Updated records: {updated_count}")
print(f"Skipped records: {skipped_count}")