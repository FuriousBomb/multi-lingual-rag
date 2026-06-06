import psycopg2
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

print("Loading embedding model...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def search_database(query_text, top_k=5):
    """Embeds query and searches database for top 5 matches."""
    query_embedding = model.encode(query_text).tolist()

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    search_sql = """
        SELECT d_name, chunk_text, 1 - (embedding <=> %s::vector) AS similarity 
        FROM docs 
        ORDER BY similarity DESC 
        LIMIT %s;
    """
    
    cur.execute(search_sql, (query_embedding, top_k))
    results = cur.fetchall()

    print("\n" + "="*50)
    print("--- TOP MATCHES ---")
    if not results:
        print("No documents found.")
        
    for i, row in enumerate(results):
        print(f"\nResult {i+1} (Score: {row[2]:.4f}) | File: {row[0]}")
        print(f"Text: {row[1]}")
        
    print("="*50 + "\n")

    cur.close()
    conn.close()

# --- EXECUTION (Interactive Loop) ---
if __name__ == "__main__":
    print("\n" + "*"*40)
    print("  RAG SEMANTIC SEARCH ENGINE READY")
    print("*"*40)
    
    while True:
        user_query = input("Enter your search query (or type 'exit' to quit): ")
        if user_query.lower().strip() == 'exit':
            print("Shutting down search engine. Goodbye!")
            break
            
        if user_query.strip():
            search_database(user_query)