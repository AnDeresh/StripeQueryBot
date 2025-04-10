import os
import pickle
import faiss

# Define the base directory of the project (assuming this file is in the "tests" folder)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Updated file paths
INDEX_FILE = os.path.join(BASE_DIR, "vectorstore", "index.faiss")
META_FILE = os.path.join(BASE_DIR, "vectorstore", "docs.pkl")

# Loading the FAISS index
index = faiss.read_index(INDEX_FILE)
print(f"[✓] Loaded FAISS index. Total vectors: {index.ntotal}")

# Loading the metadata
with open(META_FILE, "rb") as f:
    data = pickle.load(f)

texts = data["texts"]
metadatas = data["metadatas"]

print(f"[✓] Loaded metadata: {len(texts)} chunks")
print("[+] Sample:")
print("Text:", texts[0][:300], "...")
print("Source:", metadatas[0]["source"])
