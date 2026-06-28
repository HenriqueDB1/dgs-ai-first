import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Carrega .env do próprio diretório da iteração
_ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=_ENV_PATH)

CHROMA_DIR      = os.getenv("CHROMA_DIR")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
TOP_K           = int(os.getenv("TOP_K", 5))

# Modelo compartilhado (carregado uma vez por sessão)
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

# ─── Função principal ─────────────────────────────────────────────

def buscar(pergunta: str, top_k: int = TOP_K) -> list[dict]:
    """
    Recebe uma pergunta em texto e retorna os top_k chunks mais
    semanticamente próximos armazenados no ChromaDB.

    Nota: a query é codificada como texto puro (sem prefixo de título),
    pois representa a pergunta em linguagem natural do atendente.
    Os chunks foram indexados com prefixo "Documento/Seção" para
    melhorar a associação semântica — isso é a mudança central da Iteração 2.
    """
    model = get_model()
    embedding = model.encode(pergunta).tolist()

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection("novatech_v2")

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


# ─── Teste rápido ─────────────────────────────────────────────────

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
            print(f"[{i+1}] score={c['score']} | {c['source']} > {c['section'][:60]}")
            print(f"    {c['text'][:200]}...")
