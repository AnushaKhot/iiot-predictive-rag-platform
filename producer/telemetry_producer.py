import json
import random
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

MACHINES = ["KRONES-LINE-01", "KRONES-LINE-02"]

print("Starting IIoT Telemetry Ingestion Stream...")

while True:
    for machine_id in MACHINES:
        # Simulate normal data with intermittent critical spikes
        temp = random.uniform(65.0, 95.0)
        vibration = random.uniform(0.1, 4.5)
        
        status = "CRITICAL" if temp > 88.0 or vibration > 3.8 else "NORMAL"
        error_code = "ERR-TEMP-901" if temp > 88.0 else ("ERR-VIB-402" if vibration > 3.8 else "NONE")

        payload = {
            "machine_id": machine_id,
            "timestamp": time.time(),
            "temperature_c": round(temp, 2),
            "vibration_mm_s": round(vibration, 2),
            "status": status,
            "error_code": error_code
        }

        producer.send('machine-telemetry', value=payload)
        
        if status == "CRITICAL":
            print(f"[ALERT TRIGGERED] Anomalous stream detected: {payload}")
            
    time.sleep(2)