import json
from datetime import datetime
from zoneinfo import ZoneInfo

import joblib
import pandas as pd
from pymongo import MongoClient
import paho.mqtt.client as mqtt

# -----------------------------
# MQTT CONFIG
# -----------------------------
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "stressmonitor/+/readings"

# -----------------------------
# MONGO CONFIG
# -----------------------------
MONGO_URI = "mongodb+srv://dayanapriyak_db_user:Q0nXlbKhQ64tLcRz@cluster1.npcj8bx.mongodb.net/iot_project?retryWrites=true&w=majority"

DB_NAME = "iot_project"
COLLECTION_NAME = "sensor_readings"

# -----------------------------
# MODEL ARTIFACTS
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
mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]

print("Connected to MongoDB.")

# -----------------------------
# VALIDATION CONFIG
# -----------------------------
IR_GATE_THRESHOLD = 50000.0


def is_valid(data):
    return (
        data.get("temperature_c", -999) != -999
        and float(data.get("ir_value", 0)) > IR_GATE_THRESHOLD
        and float(data.get("red_value", 0)) > 0
        and float(data.get("sound_rms", -1)) >= 0
        and data.get("temp_read_success") is True
        and data.get("pulse_read_success") is True
        and data.get("audio_read_success") is True
    )


def build_feature_df(data):
    row = {
        "temperature": float(data["temperature_c"]),
        "ir": float(data["ir_value"]),
        "red": float(data["red_value"]),
        "sound_rms": float(data["sound_rms"]),
        "ir_red_ratio": float(data["ir_red_ratio"]),
        "sound_peak": float(data["sound_peak"]),
        "sound_std": float(data["sound_window_std"]),
    }

    feature_df = pd.DataFrame([row])
    feature_df = feature_df[feature_cols]

    return feature_df


def predict_ml_outputs(data):
    feature_df = build_feature_df(data)

    scaled_features = scaler.transform(feature_df)

    stress_state = stress_model.predict(scaled_features)[0]

    anomaly_label = int(anomaly_model.predict(scaled_features)[0])
    anomaly_flag = anomaly_label == -1

    stress_text = str(stress_state).lower()

    ml_alert = (
        "high" in stress_text
        or "unusual" in stress_text
        or anomaly_flag
    )

    return {
        "stress_state": str(stress_state),
        "ml_alert": bool(ml_alert),
        "anomaly_flag": bool(anomaly_flag),
        "anomaly_label": anomaly_label,
        "model_source": "live_backend",
    }


def build_mongo_doc(data):
    now_colombo = datetime.now(ZoneInfo("Asia/Colombo"))
    timestamp_local = now_colombo.strftime("%Y-%m-%d %H:%M:%S")

    ml_outputs = predict_ml_outputs(data)

    doc = {
        "device_id": data["device_id"],
        "timestamp": now_colombo,
        "timestamp_local": timestamp_local,

        "sensor_ids": {
            "temperature": data["temp_sensor_id"],
            "pulse": data["pulse_sensor_id"],
            "audio": data["audio_sensor_id"],
        },

        "readings": {
            "temperature_c": float(data["temperature_c"]),
            "ir_value": float(data["ir_value"]),
            "red_value": float(data["red_value"]),
            "sound_rms": float(data["sound_rms"]),
        },

        "features": {
            "ir_red_ratio": float(data["ir_red_ratio"]),
            "sound_peak": float(data["sound_peak"]),
            "sound_window_std": float(data["sound_window_std"]),
        },

        "health": {
            "temp_read_success": bool(data["temp_read_success"]),
            "pulse_read_success": bool(data["pulse_read_success"]),
            "audio_read_success": bool(data["audio_read_success"]),
            "temp_error_count": int(data["temp_error_count"]),
            "pulse_error_count": int(data["pulse_error_count"]),
            "audio_error_count": int(data["audio_error_count"]),
        },

        "session_id": data.get("session_id", "live_stream"),

        "ml_outputs": ml_outputs,
    }

    return doc


# -----------------------------
# MQTT CALLBACKS
# -----------------------------
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("\nReceived MQTT message")
        print(data)

        if not is_valid(data):
            print("Rejected invalid data. Not inserted into MongoDB.")
            return

        doc = build_mongo_doc(data)

        result = collection.insert_one(doc)

        print("Inserted into MongoDB")
        print("Inserted ID:", result.inserted_id)
        print("Stress State:", doc["ml_outputs"]["stress_state"])
        print("ML Alert:", doc["ml_outputs"]["ml_alert"])
        print("Anomaly:", doc["ml_outputs"]["anomaly_flag"])

    except Exception as e:
        print("Error while processing MQTT message:", e)


# -----------------------------
# START MQTT CLIENT
# -----------------------------
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("Listening for MQTT messages...")
mqtt_client.loop_forever()