# **StripeQueryBot: RAG System for Stripe API with LLaMA**

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions based on the Stripe API documentation. It uses the LLaMA model locally via Ollama for question answering, and a FAISS index for efficient document retrieval.

## **How to Run**

### 1. **Prerequisites**
- Python 3.10+
- Installed [Ollama](https://ollama.com/)
- Download the LLaMA model using `ollama pull llama3`
- Docker (optional for containerized deployment)

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

### 5. **Docker (Optional)**
If you want to containerize the application using Docker, you can follow these steps:

1. **Build the Docker image:**
   ```bash
   docker build -t llm_stripe_rag .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -p 8000:8000 llm_stripe_rag
   ```

---

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
