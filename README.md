# IIoT Predictive Maintenance & RAG Diagnostics Platform

An enterprise-grade, event-driven IIoT diagnostic platform designed to process real-time industrial machinery sensor telemetry and execute automated Retrieval-Augmented Generation (RAG) for root-cause analysis (RCA).

Built specifically to simulate high-throughput packaging line operations  by catching operational anomalies in streaming sensor telemetry and mapping diagnostic error codes against technical equipment manuals.

---

## 🏗 System Architecture

[ Telemetry Producer ] 
        │ (Simulated Sensor Stream: Temp, Vibration)
        ▼
[ Apache Kafka Broker ] ──► (Topic: 'machine-telemetry')
        │
        ▼ (Filters 'CRITICAL' Events)
[ Telemetry Consumer ]
        │
        ▼ (POST /analyze)
[ FastAPI Microservice ]
        │
        ├──► [ Hugging Face Embeddings ] (all-MiniLM-L6-v2)
        │
        ├──► [ Qdrant Vector DB ] (Semantic Search on Technical Manuals)
        │
        └──► [ Agentic RCA Engine ] ──► Automated Diagnostic Report Output

🛠 Tech Stack
Primary Languages: 
1. Python 3.12
2. Event Streaming & Messaging: Apache Kafka, Apache Zookeeper
3. AI / ML / RAG Engine: LangChain, Hugging Face Transformers (sentence-transformers/all-MiniLM-L6-v2), Qdrant Vector Store
4. Microservices & APIs: FastAPI, Uvicorn, Pydantic
5. Containerization & Ops: Docker, Docker Compose

🚀 Key Features
1. Real-Time Sensor Ingestion Stream: Simulated IIoT telemetry producer broadcasting temperature and vibration metrics across multi-line equipment configurations via Apache Kafka.
2. Automated Anomaly Interception: Asynchronous Kafka consumer service intercepting CRITICAL machine threshold spikes ($>88^\circ\text{C}$ or $>3.8\text{ mm/s}$ vibration).
3. Semantic RAG Diagnostic Mapping: Vector search mapping incoming error codes (ERR-TEMP-901, ERR-VIB-402) to technical operating manuals stored in Qdrant in-memory vector storage.
4. Decoupled Microservice Architecture: Modular ingestion, processing, and vector search services orchestrated using Docker Compose for sub-200ms diagnostic processing latency.


📁 Repository Structure
<img width="707" height="297" alt="image" src="https://github.com/user-attachments/assets/38a26461-ebf8-450a-8f29-a89b70d528c3" />




💻 Local Setup & Execution Guide
Prerequisites
Docker Desktop installed and running
Python 3.10+
Git

1. Clone the Repository & Start Infrastructure
   git clone [https://github.com/AnushaKhot/iiot-predictive-rag-platform.git](https://github.com/AnushaKhot/iiot-predictive-rag-platform.git)
cd iiot-predictive-rag-platform

# Spin up Zookeeper, Kafka, and Qdrant containers
docker-compose up -d

2. Set Up Virtual Environment & Dependencies
   python -m venv venv

# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
pip install langchain-qdrant langchain-huggingface sentence-transformers kafka-python-ng

3. Launch Services
   Terminal 1 (FastAPI RAG Service):
   uvicorn rca_service.app:app --reload --port 8000
   API documentation available at http://127.0.0.1:8000/docs

   Terminal 2 (Telemetry Ingestion Stream):
   python producer/telemetry_producer.py


   Terminal 3 (Kafka Anomaly Consumer):
   python rca_service/consumer.py


📡 Sample API Payload & Output
Endpoint: POST /analyze
Request Payload:
{
  "machine_id": "XYZ-LINE-01",
  "temperature_c": 92.5,
  "vibration_mm_s": 2.1,
  "error_code": "ERR-TEMP-901"
}

Response Payload:
{
  "machine_id": "XYZ-LINE-01",
  "error_code": "ERR-TEMP-901",
  "status": "ANALYZED",
  "retrieved_manual_context": "EQUIPMENT: XYZ Modulfill VFS\nERROR CODE: ERR-TEMP-901\nDESCRIPTION: Main drive shaft bearing overheating beyond standard operational range.\nROOT CAUSE: Lubrication seal degradation leading to high mechanical friction.",
  "agent_recommendation": "CRITICAL ALERT on KRONES-LINE-01. Inspect according to code ERR-TEMP-901. Action required based on telemetry: Temp=92.5C, Vibration=2.1mm/s."
}
