import pickle
import faiss

# Files
INDEX_FILE = "vectorstore/index.faiss"
META_FILE = "vectorstore/docs.pkl"

# Downloading the index
index = faiss.read_index(INDEX_FILE)
print(f"[✓] Loaded FAISS index. Total vectors: {index.ntotal}")

# Meta-data download
with open(META_FILE, "rb") as f:
    data = pickle.load(f)

texts = data["texts"]
metas = data["metadatas"]

print(f"[✓] Loaded metadata: {len(texts)} chunks")
print("[+] Sample:")
print("Text:", texts[0][:300], "...")
print("Source:", metas[0]["source"])
