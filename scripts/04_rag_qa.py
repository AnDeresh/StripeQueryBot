import os
import faiss
import pickle
import requests

from sentence_transformers import SentenceTransformer

# Define the base directory (project root), assuming this script is in the "scripts" folder.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === CONFIG ===
INDEX_PATH = os.path.join(BASE_DIR, "vectorstore", "index.faiss")
DOCS_PATH = os.path.join(BASE_DIR, "vectorstore", "docs.pkl")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# === LOAD VECTOR INDEX ===
print("[1] Loading index and metadata...")
index = faiss.read_index(INDEX_PATH)
with open(DOCS_PATH, "rb") as f:
    data = pickle.load(f)
texts = data["texts"]
metadatas = data["metadatas"]

# === LOAD EMBEDDING MODEL ===
print("[2] Loading embedding model...")
embedder = SentenceTransformer(EMBED_MODEL_NAME)

# === RAG FUNCTION ===
def ask_rag(query: str):
    print(f"\n[✓] Your question: {query}")

    # [A] Embed the query
    query_embedding = embedder.encode(query).astype("float32")

    # [B] Search in FAISS
    D, I = index.search(query_embedding.reshape(1, -1), TOP_K)
    matched_chunks = [texts[i] for i in I[0]]

    # [C] Build the prompt
    context = "\n\n".join(matched_chunks)
    prompt = f"""You are a helpful assistant with access to Stripe API documentation.

Context:
{context}

Answer the following question based only on the context above.

Question: {query}
Answer:"""

    # [D] Call Ollama
    print("[3] Querying LLM via Ollama...")
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })
    if response.status_code == 200:
        result = response.json()
        answer = result.get("response", "[No answer received]").strip()
        print("\n[🤖] Answer:")
        print(answer)
    else:
        print("[!] Error querying Ollama:", response.text)

# === MAIN ===
if __name__ == "__main__":
    while True:
        try:
            user_input = input("\nAsk a question (or type 'exit'): ").strip()
            if user_input.lower() in ("exit", "quit"):
                break
            ask_rag(user_input)
        except KeyboardInterrupt:
            break
