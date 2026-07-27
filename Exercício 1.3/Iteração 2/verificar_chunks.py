import chromadb
from dotenv import load_dotenv
import os

_ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=_ENV_PATH)

client = chromadb.PersistentClient(path=os.getenv("CHROMA_DIR"))
col = client.get_collection("novatech_v2")
results = col.get(limit=30, include=["metadatas"])

for m in results["metadatas"]:
    print(f"{m['source'][:30]:<32} | {m['section']}")
