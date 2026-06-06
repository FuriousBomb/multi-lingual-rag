Basic RAG Data Store: Document Import and Semantic Search 

This project implements a localized, high-performance backend component for a Retrieval-Augmented Generation (RAG) pipeline. It handles document ingestion, automatic text chunking, multilingual vector embedding generation, and semantic vector similarity searches using PostgreSQL and the `pgvector` extension.

Instead of relying on simple, exact-keyword matching, this system computes the semantic meaning of queries to surface the most contextually relevant document sections. It features cross-lingual capabilities, allowing users to query English documents using Hindi or Malayalam, and vice versa.

---

## System Architecture

The application is engineered with a decoupled, modular pipeline split into three clear operational layers:

1. 
**Data Ingestion Layer:** Reads localized source documents (`.txt`, `.pdf`, `.docx`), normalizes and splits raw text into manageable chunks, and passes strings downstream.


2. 
**Embedding & Core AI Engine:** Leverages a local Sentence-Transformers model to convert text strings into high-density, 384-dimensional conceptual vectors.


3. 
**Vector Database Layer:** Utilizes a containerized PostgreSQL database equipped with `pgvector` to store chunks alongside their vector data and run ultra-fast Cosine Distance (`<=>`) comparison queries.



---

Tech Stack 

* 
**Language:** Python 3.x 


* 
**Database:** PostgreSQL (v16) with `pgvector` extension 


* 
**Embedding Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (Upgraded for robust Hindi and Malayalam cross-lingual indexing) 


* 
**Document Parsing:** `pypdf`, `python-docx` 


* **Containerization:** Docker / Docker Desktop

---

Setup & Installation 

1. Clone the Repository 

```bash
git clone https://github.com/FuriousBomb/multi-lingual-rag.git
cd pipeline

```

### 2. Spin Up the Vector Database (Docker Route)

Ensure Docker Desktop is running on your machine. Execute this command in your terminal to deploy a pre-configured PostgreSQL environment containing the `pgvector` module: 

```bash
docker run --name rag-postgres -e POSTGRES_PASSWORD=admin -p 5432:5432 -d pgvector/pgvector:pg16

```

3. Initialize the Database Schema 

Connect to your database instance via a visual tool (like DBeaver or pgAdmin) or execute it directly using the container terminal:

```bash
docker exec -it rag-postgres psql -U postgres

```

Run the following initialization script to enable the extension and build the target datastore structure:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    d_name VARCHAR(255) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

*(Type `\q` to exit the database prompt).*

### 4. Configure Python Environment & Dependencies

Create and activate an isolated virtual environment on your host machine, then install the mandatory runtime packages:

```bash
# Create environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Install required libraries
pip install sentence-transformers psycopg2-binary pypdf python-docx

```

---

## 💻 Usage

📥 Ingesting Custom Documents 

You can dynamically parse, chunk, embed, and store `.txt`, `.pdf`, or `.docx` documents by pointing the ingestion script directly to your file path:

```bash
python docs_import.py your_document.pdf

```

🔍 Executing Semantic Search 

Launch the interactive terminal query interface:

```bash
python semantic_search.py

```

Type your natural language query when prompted. The engine will display the top 5 closest conceptual fragments sorted strictly by mathematical similarity scores. Type `exit` to terminate the process.

---

## 📂 Project Structure

```text
├── venv/                  # Python Virtual Environment variables
├── test_results/          # test results from previous sample dataset
├── import_docs.py         # Unified ingestion tool (Extracts, chunks, embeds, stores) 
├── search_docs.py         # Interactive, cross-lingual vector search runtime loop
├── sample_dataset.pdf     # sample pdf with hindi and english data (SEBI regulations article)
├── README.md              # Setup instructions and documentation
└── architecture.png       # High-level system interaction schematic diagram

```
