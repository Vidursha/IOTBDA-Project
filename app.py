from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict

MONGO_URI = "mongodb+srv://dayanapriyak_db_user:Q0nXlbKhQ64tLcRz@cluster1.npcj8bx.mongodb.net/iot_project?retryWrites=true&w=majority"

DB_NAME = "iot_project"
COLLECTION_NAME = "sensor_readings"

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def clean_doc(doc):
    if not doc:
        return None

    doc["_id"] = str(doc["_id"])

    if isinstance(doc.get("timestamp"), datetime):
        doc["timestamp"] = doc["timestamp"].isoformat()

    return doc


def stress_score_from_state(state):
    state = str(state)
    if "High" in state:
        return 2
    if "Moderate" in state:
        return 1
    if "Low" in state:
        return 0
    return None


@app.route("/")
def home():
    return jsonify({
        "message": "IoT Stress Monitoring API is running",
        "available_routes": [
            "/api/health",
            "/api/latest",
            "/api/recent",
            "/api/stress-distribution",
            "/api/alerts-summary",
            "/api/anomaly-summary",
            "/api/trends",
            "/api/summary-trends",
            "/api/health-summary"
        ]
    })


@app.route("/api/health")
def health():
    try:
        count = collection.count_documents({})
        return jsonify({
            "status": "ok",
            "mongo_connected": True,
            "record_count": count
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "mongo_connected": False,
            "error": str(e)
        })


@app.route("/api/latest")
def latest_record():
    doc = collection.find_one(sort=[("timestamp", -1)])
    return jsonify(clean_doc(doc))


@app.route("/api/recent")
def recent_records():
    docs = list(collection.find().sort("timestamp", -1).limit(25))
    return jsonify([clean_doc(doc) for doc in docs])


@app.route("/api/stress-distribution")
def stress_distribution():
    pipeline = [
        {
            "$group": {
                "_id": "$ml_outputs.stress_state",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]

    results = list(collection.aggregate(pipeline))

    data = [
        {
            "stress_state": item["_id"] if item["_id"] else "Not Scored",
            "count": item["count"]
        }
        for item in results
    ]

    return jsonify(data)


@app.route("/api/alerts-summary")
def alerts_summary():
    total = collection.count_documents({})
    alerts = collection.count_documents({"ml_outputs.ml_alert": True})

    return jsonify({
        "total_records": total,
        "alert_records": alerts,
        "no_alert_records": total - alerts,
        "alert_percentage": round((alerts / total) * 100, 2) if total else 0
    })


@app.route("/api/anomaly-summary")
def anomaly_summary():
    total = collection.count_documents({})
    anomalies = collection.count_documents({"ml_outputs.anomaly_flag": True})

    return jsonify({
        "total_records": total,
        "anomaly_records": anomalies,
        "normal_records": total - anomalies,
        "anomaly_percentage": round((anomalies / total) * 100, 2) if total else 0
    })


@app.route("/api/trends")
def trends():
    docs = list(
        collection.find(
            {},
            {
                "_id": 0,
                "timestamp": 1,
                "readings.temperature_c": 1,
                "readings.sound_rms": 1,
                "features.ir_red_ratio": 1,
                "ml_outputs.stress_state": 1,
                "ml_outputs.ml_alert": 1,
                "ml_outputs.anomaly_flag": 1
            }
        )
        .sort("timestamp", 1)
        .limit(1000)
    )

    data = []

    for doc in docs:
        ts = doc.get("timestamp")
        if isinstance(ts, datetime):
            ts = ts.isoformat()

        readings = doc.get("readings", {})
        features = doc.get("features", {})
        ml = doc.get("ml_outputs", {})

        stress_state = ml.get("stress_state", "Not Scored")

        data.append({
            "timestamp": ts,
            "temperature": readings.get("temperature_c"),
            "sound_rms": readings.get("sound_rms"),
            "ir_red_ratio": features.get("ir_red_ratio"),
            "stress_state": stress_state,
            "stress_score": stress_score_from_state(stress_state),
            "ml_alert": ml.get("ml_alert", False),
            "anomaly_flag": ml.get("anomaly_flag", False)
        })

    return jsonify(data)


@app.route("/api/summary-trends")
def summary_trends():
    docs = list(
        collection.find(
            {},
            {
                "_id": 0,
                "timestamp": 1,
                "readings.temperature_c": 1,
                "readings.sound_rms": 1,
                "readings.ir_value": 1,
                "readings.red_value": 1,
                "features.ir_red_ratio": 1,
                "ml_outputs.stress_state": 1,
                "ml_outputs.ml_alert": 1,
                "ml_outputs.anomaly_flag": 1,
            }
        ).sort("timestamp", 1)
    )

    buckets = defaultdict(lambda: {
        "stress_scores": [],
        "temperatures": [],
        "sound_values": [],
        "ratios": [],
        "alert_count": 0,
        "anomaly_count": 0,
        "record_count": 0
    })

    for doc in docs:
        ts = doc.get("timestamp")
        if not isinstance(ts, datetime):
            continue

        bucket_minute = 0 if ts.minute < 30 else 30
        bucket_time = ts.replace(minute=bucket_minute, second=0, microsecond=0)
        key = bucket_time.isoformat()

        readings = doc.get("readings", {})
        features = doc.get("features", {})
        ml = doc.get("ml_outputs", {})

        stress_state = ml.get("stress_state", "")
        stress_score = stress_score_from_state(stress_state)

        if stress_score is not None:
            buckets[key]["stress_scores"].append(stress_score)

        if readings.get("temperature_c") is not None:
            buckets[key]["temperatures"].append(readings["temperature_c"])

        if readings.get("sound_rms") is not None:
            buckets[key]["sound_values"].append(readings["sound_rms"])

        if features.get("ir_red_ratio") is not None:
            buckets[key]["ratios"].append(features["ir_red_ratio"])

        if ml.get("ml_alert") is True:
            buckets[key]["alert_count"] += 1

        if ml.get("anomaly_flag") is True:
            buckets[key]["anomaly_count"] += 1

        buckets[key]["record_count"] += 1

    output = []

    for time_key, values in buckets.items():
        output.append({
            "timestamp": time_key,
            "avg_stress_score": round(sum(values["stress_scores"]) / len(values["stress_scores"]), 3) if values["stress_scores"] else None,
            "avg_temperature": round(sum(values["temperatures"]) / len(values["temperatures"]), 3) if values["temperatures"] else None,
            "avg_sound_rms": round(sum(values["sound_values"]) / len(values["sound_values"]), 3) if values["sound_values"] else None,
            "avg_ir_red_ratio": round(sum(values["ratios"]) / len(values["ratios"]), 3) if values["ratios"] else None,
            "alert_count": values["alert_count"],
            "anomaly_count": values["anomaly_count"],
            "record_count": values["record_count"]
        })

    output.sort(key=lambda x: x["timestamp"])
    return jsonify(output)


@app.route("/api/health-summary")
def health_summary():
    total = collection.count_documents({})

    temp_success = collection.count_documents({"health.temp_read_success": True})
    pulse_success = collection.count_documents({"health.pulse_read_success": True})
    audio_success = collection.count_documents({"health.audio_read_success": True})

    pipeline = [
        {
            "$group": {
                "_id": None,
                "temp_errors": {"$sum": "$health.temp_error_count"},
                "pulse_errors": {"$sum": "$health.pulse_error_count"},
                "audio_errors": {"$sum": "$health.audio_error_count"}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))
    errors = result[0] if result else {}

    return jsonify({
        "total_records": total,
        "sensor_success_rates": [
            {
                "sensor": "Temperature",
                "success_rate": round((temp_success / total) * 100, 2) if total else 0
            },
            {
                "sensor": "Pulse",
                "success_rate": round((pulse_success / total) * 100, 2) if total else 0
            },
            {
                "sensor": "Audio",
                "success_rate": round((audio_success / total) * 100, 2) if total else 0
            }
        ],
        "error_counts": [
            {
                "sensor": "Temperature",
                "errors": errors.get("temp_errors", 0)
            },
            {
                "sensor": "Pulse",
                "errors": errors.get("pulse_errors", 0)
            },
            {
                "sensor": "Audio",
                "errors": errors.get("audio_errors", 0)
            }
        ]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)