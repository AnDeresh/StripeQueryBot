from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import faiss
import pickle
import requests
from sentence_transformers import SentenceTransformer

# === CONFIG ===
INDEX_PATH = "vectorstore/index.faiss"
DOCS_PATH = "vectorstore/docs.pkl"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

# === LOAD COMPONENTS ===
index = faiss.read_index(INDEX_PATH)
with open(DOCS_PATH, "rb") as f:
    data = pickle.load(f)
texts = data["texts"]

embedder = SentenceTransformer(EMBED_MODEL_NAME)

# === FASTAPI SETUP ===
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    try:
        # [1] Embed the query
        query_embedding = embedder.encode(query.question).astype("float32")

        # [2] Search FAISS
        D, I = index.search(query_embedding.reshape(1, -1), TOP_K)
        matched_chunks = [texts[i] for i in I[0]]

        # [3] Build prompt
        context = "\n\n".join(matched_chunks)
        prompt = f"""You are a helpful assistant with access to Stripe API documentation.

Context:
{context}

Answer the following question based only on the context above.

Question: {query.question}
Answer:"""

        # [4] Query Ollama
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        result = response.json()

        return {"answer": result.get("response", "No response from model.")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05_rag_api:app", host="127.0.0.1", port=8000, reload=True)
