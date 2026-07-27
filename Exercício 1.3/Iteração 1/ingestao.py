import os
import re
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# ─── Configurações ────────────────────────────────────────────────
load_dotenv()

DOCS_DIR = os.getenv("DOCS_DIR")
CHROMA_DIR = os.getenv("CHROMA_DIR")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))
OVERLAP_TOKENS = int(os.getenv("OVERLAP_TOKENS", 50))
# Regra base: 0,75 palavras/token (inglês). Português gera ~25% mais tokens,
# ou seja, cada token representa 25% menos palavras: 0,75 × 0,75 = ~0,56 ≈ 0,6.
# Referência: análise de viabilidade técnica — Exercício 1.1.
WORDS_PER_TOKEN = float(os.getenv("WORDS_PER_TOKEN", 0.6))

MAX_WORDS = int(MAX_TOKENS * WORDS_PER_TOKEN)          # 500 tokens × 0,6 = ~300 palavras
OVERLAP_WORDS = int(OVERLAP_TOKENS * WORDS_PER_TOKEN)  # 50 tokens × 0,6 = ~30 palavras

# ─── Funções de chunking ──────────────────────────────────────────

def words_count(text):
    return len(text.split())

def split_by_paragraphs_with_overlap(text, source, section):
    """
    Nível 3 — divide texto corrido por parágrafo com overlap.
    Usado quando uma ### ainda ultrapassa MAX_WORDS.
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    current = []
    current_words = 0

    for para in paragraphs:
        para_words = words_count(para)

        if current_words + para_words > MAX_WORDS and current:
            chunks.append('\n\n'.join(current))
            overlap_text = ' '.join(' '.join(current).split()[-OVERLAP_WORDS:])
            current = [overlap_text, para]
            current_words = words_count(overlap_text) + para_words
        else:
            current.append(para)
            current_words += para_words

    if current:
        chunks.append('\n\n'.join(current))

    return [
        {
            "text": c,
            "source": source,
            "section": f"{section} (parte {i+1})"
        }
        for i, c in enumerate(chunks)
    ]

def split_section(text, source, section_title):
    """
    Nível 2 — divide por ###.
    Se ainda ultrapassar, chama nível 3.
    """
    subsections = re.split(r'\n(?=### )', text)
    chunks = []

    for sub in subsections:
        sub = sub.strip()
        if not sub:
            continue

        lines = sub.split('\n')
        sub_title = lines[0].replace('###', '').strip()
        sub_body = '\n'.join(lines[1:]).strip()
        full_label = f"{section_title} > {sub_title}"

        if words_count(sub_body) <= MAX_WORDS:
            chunks.append({
                "text": sub_body,
                "source": source,
                "section": full_label
            })
        else:
            chunks.extend(split_by_paragraphs_with_overlap(sub_body, source, full_label))

    return chunks

def extract_doc_header(content):
    """
    Extrai o conteúdo do nível # (cabeçalho do documento) — título, metadados e avisos.
    Esse conteúdo não vira chunk, mas é preservado como metadado em todos os chunks
    do documento para manter contexto sobre a natureza da fonte (ex: FAQ informal).
    """
    match = re.match(r'^(#[^#].*?)(?=\n## |\Z)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def chunk_document(filepath):
    """
    Nível 1 — divide por ##.
    Se ultrapassar, verifica se tem ### (nível 2) ou vai direto ao nível 3.
    O cabeçalho # é extraído e adicionado como metadado em todos os chunks.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)

    # extrai cabeçalho do documento (nível #) como metadado
    doc_header = extract_doc_header(content)

    sections = re.split(r'\n(?=## )', content)
    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # ignora o bloco do cabeçalho # que já foi extraído
        if not section.startswith('## '):
            continue

        lines = section.split('\n')
        section_title = lines[0].replace('##', '').strip()
        section_body = '\n'.join(lines[1:]).strip()

        if words_count(section_body) <= MAX_WORDS:
            chunks.append({
                "text": section_body,
                "source": filename,
                "section": section_title,
                "doc_header": doc_header
            })
        elif '### ' in section_body:
            for c in split_section(section_body, filename, section_title):
                c["doc_header"] = doc_header
                chunks.append(c)
        else:
            for c in split_by_paragraphs_with_overlap(section_body, filename, section_title):
                c["doc_header"] = doc_header
                chunks.append(c)

    return chunks

# ─── Ingestão ─────────────────────────────────────────────────────

def ingerir():
    print("Carregando modelo de embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Inicializando ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection("novatech")
    except:
        pass
    collection = client.create_collection("novatech")

    arquivos = [f for f in os.listdir(DOCS_DIR) if f.endswith('.md')]
    total_chunks = 0

    for arquivo in arquivos:
        filepath = os.path.join(DOCS_DIR, arquivo)
        print(f"\nProcessando: {arquivo}")

        chunks = chunk_document(filepath)
        print(f"  → {len(chunks)} chunks gerados")

        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk["text"]).tolist()
            doc_id = f"{arquivo}_{i}"

            collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[{
                    "source": chunk["source"],
                    "section": chunk["section"],
                    "doc_header": chunk.get("doc_header", "")
                }]
            )
            print(f"  [{i+1}/{len(chunks)}] {chunk['section'][:60]}")
            total_chunks += 1

    print(f"\n✅ Ingestão concluída: {total_chunks} chunks armazenados no ChromaDB")

if __name__ == "__main__":
    ingerir()
