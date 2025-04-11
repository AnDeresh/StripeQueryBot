import faiss
import pickle
import requests
import os

from sentence_transformers import SentenceTransformer

# === CONFIG ===
INDEX_PATH = "vectorstore/index.faiss"
DOCS_PATH = "vectorstore/docs.pkl"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
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

        
# === EXAMPLE INTERACTIONS ===
# Example 1:
# Question: Як створити платіж через Stripe API?
# Answer:
# To make a payment through Stripe, you can use the `charges.create` endpoint in the Stripe API. This endpoint allows you to create a new charge on a customer's credit card.
# Example:
# curl https://api.stripe.com/v1/charges \
# -u "sk_test_..." \
# -d "amount=1000&currency=usd&customer=cus_12345678"

# Example 2:
# Question: Що таке customer у Stripe?
# Answer:
# A customer in Stripe represents an entity (user or organization) that you can charge, store payment methods for, and track billing history. You create a customer object via the Customers API and can attach payment sources, email, metadata, etc.