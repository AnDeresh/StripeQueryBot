# RAG system for Stripe API with LLaMA (via Ollama)

This project implements a Retrieval-Augmented Generation (RAG) approach for working with Stripe API documentation, using a local LLaMA model running via [Ollama](https://ollama.com/).

## How to Run

### 1. Prerequisites
- Python 3.10+
- Installed [Ollama](https://ollama.com/)
- Download the LLaMA model using `ollama pull llama3`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Service
```bash
python 04_rag_qa.py
```

## How It Works
1. **Documentation Load** — Stripe documentation is fetched and split into text chunks.
2. **Vectorization** — Each chunk is vectorized using `sentence-transformers`.
3. **Indexing with FAISS** — Vectors are stored in a FAISS database for fast retrieval.
4. **User Query** — The query is converted into an embedding, and the top relevant chunks are retrieved.
5. **Prompt Construction** — A prompt is created using the relevant documentation fragments.
6. **LLaMA Call** — The prompt is passed to LLaMA via the Ollama API to generate an answer.

## Technologies Used
- **Language:** Python
- **Model:** LLaMA 3 via Ollama
- **Vector Store:** FAISS
- **Libraries:**
  - `sentence-transformers`
  - `requests`
  - `faiss-cpu`
  - `torch`

## Example Queries

### Example 1
**Question:** How to create a payment using the Stripe API?

**Answer:**
To make a payment through Stripe, you can use the `charges.create` endpoint. Example:

```bash
curl https://api.stripe.com/v1/charges \
-u "sk_test_7mJuPfZ...JkrANrFrcDqC:" \
-H "Stripe-Version: 2025-03-31.basil" \
-d "amount=1000&currency=usd&customer=cus_12345678"
```

### Example 2
**Question:** What is a customer in Stripe?

**Answer:**
A customer object represents a user of your application. It is used to manage recurring billing, payment methods, and associated charges in the Stripe ecosystem.