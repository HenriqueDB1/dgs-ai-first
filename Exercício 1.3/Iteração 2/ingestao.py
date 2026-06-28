import os
import re
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# ─── Configurações ────────────────────────────────────────────────
# Carrega .env do próprio diretório da iteração
_ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=_ENV_PATH)

DOCS_DIR       = os.getenv("DOCS_DIR")
CHROMA_DIR     = os.getenv("CHROMA_DIR")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
MAX_TOKENS     = int(os.getenv("MAX_TOKENS", 500))
OVERLAP_TOKENS = int(os.getenv("OVERLAP_TOKENS", 50))
# Regra base: 0,75 palavras/token (inglês). Português gera ~25% mais tokens,
# ou seja, cada token representa 25% menos palavras: 0,75 × 0,75 = ~0,56 ≈ 0,6.
WORDS_PER_TOKEN = float(os.getenv("WORDS_PER_TOKEN", 0.6))

MAX_WORDS    = int(MAX_TOKENS * WORDS_PER_TOKEN)       # ~300 palavras
OVERLAP_WORDS = int(OVERLAP_TOKENS * WORDS_PER_TOKEN)  # ~30 palavras

# ─── Funções de chunking (iguais à Iteração 1) ───────────────────

def words_count(text):
    return len(text.split())

def split_by_paragraphs_with_overlap(text, source, section):
    """Nível 3 — divide por parágrafo com overlap quando ### ultrapassa MAX_WORDS."""
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
        {"text": c, "source": source, "section": f"{section} (parte {i+1})"}
        for i, c in enumerate(chunks)
    ]

def split_section(text, source, section_title):
    """Nível 2 — divide por ###, chama nível 3 se ainda ultrapassar."""
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
            chunks.append({"text": sub_body, "source": source, "section": full_label})
        else:
            chunks.extend(split_by_paragraphs_with_overlap(sub_body, source, full_label))

    return chunks

def extract_doc_header(content):
    """Extrai o bloco # como metadado (não vira chunk)."""
    match = re.match(r'^(#[^#].*?)(?=\n## |\Z)', content, re.DOTALL)
    return match.group(1).strip() if match else ""

def chunk_document(filepath):
    """Nível 1 — divide por ##, delega para nível 2 ou 3 se necessário."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    doc_header = extract_doc_header(content)
    sections = re.split(r'\n(?=## )', content)
    chunks = []

    for section in sections:
        section = section.strip()
        if not section or not section.startswith('## '):
            continue

        lines = section.split('\n')
        section_title = lines[0].replace('##', '').strip()
        section_body = '\n'.join(lines[1:]).strip()

        if words_count(section_body) <= MAX_WORDS:
            chunks.append({"text": section_body, "source": filename,
                           "section": section_title, "doc_header": doc_header})
        elif '### ' in section_body:
            for c in split_section(section_body, filename, section_title):
                c["doc_header"] = doc_header
                chunks.append(c)
        else:
            for c in split_by_paragraphs_with_overlap(section_body, filename, section_title):
                c["doc_header"] = doc_header
                chunks.append(c)

    return chunks

# ─── Mudança 2: título da seção incluído no texto do embedding ────

def build_embedding_text(chunk):
    """
    Constrói o texto enviado ao modelo para geração do embedding.

    Na Iteração 1 o embedding era gerado apenas com o corpo do chunk,
    deixando o título da seção apenas como metadado. Isso fazia o modelo
    recuperar seções erradas dentro do documento correto (ex.: seção 3.5
    em vez de 3.1 para 'prazo de devolução').

    Aqui incluímos o nome do documento e o título da seção no texto de
    embedding, criando ponte semântica direta entre a pergunta e a seção
    correta. O texto armazenado no ChromaDB continua sendo o corpo limpo,
    para que o prompt assembly exiba conteúdo sem ruído.
    """
    doc_name = chunk["source"].replace(".md", "").replace("-", " ")
    section  = chunk["section"]
    text     = chunk["text"]
    # Copilot: sugestão de prefixo semântico para melhorar retrieval multilíngue
    return f"Documento: {doc_name}\nSeção: {section}\n\n{text}"

# ─── Ingestão ─────────────────────────────────────────────────────

def ingerir():
    print(f"Carregando modelo de embeddings: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Inicializando ChromaDB (Iteração 2)...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection("novatech_v2")
    except:
        pass
    collection = client.create_collection("novatech_v2")

    arquivos = [f for f in os.listdir(DOCS_DIR) if f.endswith('.md')]
    total_chunks = 0

    for arquivo in arquivos:
        filepath = os.path.join(DOCS_DIR, arquivo)
        print(f"\nProcessando: {arquivo}")

        chunks = chunk_document(filepath)
        print(f"  → {len(chunks)} chunks gerados")

        for i, chunk in enumerate(chunks):
            # embedding gerado com título + corpo (mudança principal)
            embedding_text = build_embedding_text(chunk)
            embedding = model.encode(embedding_text).tolist()

            # ChromaDB armazena o corpo limpo (sem o prefixo de título)
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

    print(f"\n✅ Ingestão concluída: {total_chunks} chunks armazenados (Iteração 2)")

if __name__ == "__main__":
    ingerir()
