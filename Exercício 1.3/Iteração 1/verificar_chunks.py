import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

client = chromadb.PersistentClient(path=os.getenv("CHROMA_DIR"))
col = client.get_collection("novatech")
results = col.get(limit=30, include=["metadatas"])

for m in results["metadatas"]:
    print(f"{m['source'][:30]:<32} | {m['section']}")
