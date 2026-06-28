import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# ─── Configurações ────────────────────────────────────────────────
load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_DIR")
TOP_K = int(os.getenv("TOP_K", 5))

# Modelo compartilhado (carregado uma vez por sessão)
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

# ─── Função principal ─────────────────────────────────────────────

def buscar(pergunta: str, top_k: int = TOP_K) -> list[dict]:
    """
    Recebe uma pergunta em texto e retorna os top_k chunks mais
    semanticamente próximos armazenados no ChromaDB.

    Retorna lista de dicts com:
        text      — conteúdo do chunk
        source    — arquivo de origem
        section   — seção de origem
        doc_header — cabeçalho do documento (metadado)
        score     — distância coseno (menor = mais relevante)
    """
    model = get_model()
    embedding = model.encode(pergunta).tolist()

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection("novatech")

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta.get("source", ""),
            "section": meta.get("section", ""),
            "doc_header": meta.get("doc_header", ""),
            "score": round(dist, 4)
        })

    return chunks


# ─── Teste rápido (executar diretamente) ─────────────────────────

if __name__ == "__main__":
    perguntas_teste = [
        "Qual o prazo de devolução para cliente Gold?",
        "Como calcular o frete para Manaus?",
        "O cliente diz que é Platinum. Isso existe?"
    ]

    for pergunta in perguntas_teste:
        print(f"\n{'='*60}")
        print(f"Pergunta: {pergunta}")
        print(f"{'='*60}")
        chunks = buscar(pergunta, top_k=3)
        for i, c in enumerate(chunks):
            print(f"\n[{i+1}] score={c['score']} | {c['source']} > {c['section'][:60]}")
            print(f"    {c['text'][:200]}...")
