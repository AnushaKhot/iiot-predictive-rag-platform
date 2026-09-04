import json
import time
import requests
from kafka import KafkaConsumer

FASTAPI_URL = "http://127.0.0.1:8000/analyze"

print("Connecting to Kafka Broker at localhost:9092...")

# Added api_version and request_timeout_ms to prevent hanging on Python 3.12
consumer = KafkaConsumer(
    'machine-telemetry',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    api_version=(2, 0, 0),
    request_timeout_ms=10000
)

print("Connected! Listening for IIoT Critical Telemetry Streams...")

for message in consumer:
    telemetry = message.value
    
    if telemetry.get("status") == "CRITICAL":
        payload = {
            "machine_id": telemetry["machine_id"],
            "temperature_c": telemetry["temperature_c"],
            "vibration_mm_s": telemetry["vibration_mm_s"],
            "error_code": telemetry["error_code"]
        }
        
        try:
            response = requests.post(FASTAPI_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"\n[ALERT PROCESSED] Machine: {data['machine_id']} | Code: {data['error_code']}")
                print(f"RCA Output: {data.get('agent_recommendation')}\n")
        except Exception as e:
            print(f"[ERROR] Could not connect to RCA microservice: {e}")