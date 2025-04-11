# **StripeQueryBot: RAG System for Stripe API with LLaMA**

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions based on the Stripe API documentation. It uses the LLaMA model locally via Ollama for question answering, and a FAISS index for efficient document retrieval.

## Project Structure
```plaintext
StripeQueryBot/
├── data/
│   ├── stripe_docs.json             # JSON file containing scraped documentation text
│   └── stripe_urls.json             # JSON file listing URLs collected from Stripe docs
├── vectorstore/
│   ├── docs.pkl                     # Pickled dictionary of chunked texts and metadata
│   └── index.faiss                  # FAISS index storing vector embeddings for fast retrieval
├── .gitattributes                   # Git-specific attributes (e.g., Git LFS tracking)
│
├── 01_collect_links_async.py        # Step 1. Asynchronously collect URLs from the Stripe docs homepage
├── 02_scrape_stripe_pages.py        # Step 2. Scrape each URL to retrieve full documentation text
├── 03_chunk_and_embed.py            # Step 3. Split text into chunks and embed them for FAISS indexing
├── 04_rag_qa.py                     # Step 4. Gradio-based Q&A interface using local embeddings
├── 05_rag_api.py                    # Step 5. FastAPI-based endpoint providing a Q&A API
│
├── docker-compose.yml               # Docker Compose config for running API and LLaMA servers
├── Dockerfile.app                   # Dockerfile for containerizing the main application (FastAPI/Streamlit app)
├── README.md                        # Main project documentation, setup and usage instructions
├── requirements.txt                 # Python dependencies required by the project
└── test_index.py                    # Script for testing the FAISS index and verifying loaded data
```

## **How to Run**

### 1. **Prerequisites**
- Python 3.10+
- Installed [Ollama](https://ollama.com/)
- Download the LLaMA model using `ollama pull llama3`
- Docker (optional for containerized deployment)
- If you cloned the repo, make sure to run `git lfs pull` to fetch large files (like `index.faiss` and `docs.pkl`)

### 2. **Install Dependencies**
Install the necessary Python libraries with the following command:
```bash
pip install -r requirements.txt
```

### 3. **Run the Gradio UI (Optional)**
To run a Gradio-based interface for the Q&A system:
```bash
python 04_rag_qa.py
```

### 4. **Run the FastAPI Server (Optional)**
To deploy the Q&A system as an API with FastAPI:
```bash
uvicorn 05_rag_api:app --reload
```

## 🐳 Docker (Optional)

If you want to containerize the application along with the LLaMA server, follow these steps:

---

### 1. Build & Run the Project

If you want to containerize the application along with the LLaMA server, follow these steps:

In **Terminal / CMD / PowerShell**, run:

1. **Run a Docker**
   ```bash
   docker compose up
   ```
  
This will:
- build both containers (if not already built),
- launch the FastAPI app and the LLaMA server,
- stream logs to the terminal (this terminal will remain occupied).

> Don't close this terminal! It keeps your containers running.

2. **Load the LLaMA Model**
   ```bash
   docker exec -it ollama ollama pull llama3
   ```

This downloads the LLaMA 3 model into the llama container.

> You only need to run this once. The model stays cached in the container.

3. **Access the API**
Once both containers are running and the model is loaded, you can open:
   ```bash
   http://localhost:8000/docs
   ```

**Need to restart?**
You can always stop the app with `Ctrl+C in` the first terminal, then bring it back up with:
   ```bash
   docker compose up
   ```
If you want a clean reset (remove containers, volumes, networks):
   ```bash
   docker compose down
   ```
   
## **How It Works**

1. **Documentation Load** — Fetches Stripe API documentation and splits it into text chunks.
2. **Vectorization** — Uses the `sentence-transformers` library to generate embeddings for each chunk.
3. **Indexing with FAISS** — Embeddings are stored in a FAISS index for efficient retrieval.
4. **User Query** — User input is encoded into an embedding, and the top relevant chunks are retrieved.
5. **Prompt Construction** — Relevant chunks are combined into a prompt and passed to LLaMA.
6. **LLaMA Call** — The prompt is sent to LLaMA via the Ollama API for generating an answer.
7. **Interface** — Users can interact with the system through either Gradio or FastAPI.

---

## **Technologies Used**

- **Language:** Python
- **Model:** LLaMA (via Ollama)
- **Vector Store:** FAISS
- **Interface:** Gradio / FastAPI
- **Libraries:**
  - `sentence-transformers`
  - `requests`
  - `faiss-cpu`
  - `torch`
  - `gradio`
  - `fastapi`
  - `uvicorn`

---

## **Example Queries**

### Example 1:
**Question:** How to create a payment using the Stripe API?

**Answer:**
To make a payment through Stripe, you can use the `charges.create` endpoint. Example:

```bash
curl https://api.stripe.com/v1/charges \
  -u "sk_test_7mJuPfZ...JkrANrFrcDqC" \
  -d "amount=1000&currency=usd&customer=cus_12345678"
```

### Example 2:
**Question:** What is a customer in Stripe?

**Answer:**
A customer in Stripe represents an entity (user or organization) that you can charge, store payment methods for, and track billing history. You create a customer object via the `Customers API` and can attach payment sources, email, metadata, etc.
