import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import FakeListLLM  # For local testing without an API key

app = FastAPI(title="IIoT Agentic RCA Microservice")

# Free, local CPU embeddings (no API key required)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Setup Vector Search Context
loader = TextLoader("manuals/krones_filling_machine.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)
docs = text_splitter.split_documents(documents)

# Initialize Qdrant Vector Store
vectorstore = QdrantVectorStore.from_documents(
    docs,
    embeddings,
    location=":memory:",
    collection_name="manuals"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

class AnomalyEvent(BaseModel):
    machine_id: str
    temperature_c: float
    vibration_mm_s: float
    error_code: str

@app.post("/analyze")
async def run_rca(event: AnomalyEvent):
    # Retrieve manual instructions based on error_code
    relevant_docs = retriever.invoke(event.error_code)
    manual_context = relevant_docs[0].page_content if relevant_docs else "No manual section found."

    # Formulate RCA Output
    return {
        "machine_id": event.machine_id,
        "error_code": event.error_code,
        "status": "ANALYZED",
        "retrieved_manual_context": manual_context,
        "agent_recommendation": f"CRITICAL ALERT on {event.machine_id}. Inspect according to code {event.error_code}. Action required based on telemetry: Temp={event.temperature_c}C, Vibration={event.vibration_mm_s}mm/s."
    }