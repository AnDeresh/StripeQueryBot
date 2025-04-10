import os
import json
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss

# Розмір фрагменту та перехресна накладка
CHUNK_SIZE = 250
CHUNK_OVERLAP = 30

# Визначаємо базову директорію проєкту (корінь щодо папки scripts/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Оновлені шляхи до файлів згідно нової структури
INPUT_FILE = os.path.join(BASE_DIR, "data", "stripe_docs.json")
INDEX_DIR = os.path.join(BASE_DIR, "vectorstore")
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
META_FILE = os.path.join(INDEX_DIR, "docs.pkl")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # невелика та швидка модель


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def load_docs(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_docs = json.load(f)

    chunks = []
    metadatas = []

    for doc in tqdm(raw_docs, desc="Chunking"):
        url = doc["url"]
        text = doc["content"]
        if not text.strip():
            continue

        for chunk in chunk_text(text):
            chunks.append(chunk)
            metadatas.append({"source": url})

    return chunks, metadatas


def build_faiss_index(embeddings, dimension):
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def main():
    # Створити директорію для індексу, якщо її ще немає
    os.makedirs(INDEX_DIR, exist_ok=True)

    print("[1] Loading documents and chunking...")
    chunks, metadatas = load_docs(INPUT_FILE)

    print(f"[2] Total chunks: {len(chunks)}")
    print("[3] Computing embeddings...")

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = model.encode(chunks, show_progress_bar=True)

    print("[4] Building FAISS index...")
    index = build_faiss_index(embeddings, dimension=embeddings.shape[1])

    print(f"[5] Saving index to {INDEX_FILE} and metadata to {META_FILE}")
    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump({"texts": chunks, "metadatas": metadatas}, f)

    print("[✓] Done! Ready for retrieval.")


if __name__ == "__main__":
    main()
