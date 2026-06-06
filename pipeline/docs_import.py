import psycopg2
import os
import sys
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import docx

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

# --- COMPONENT 1: Universal Text Extractor ---
def extract_text(file_path):
    """Detects file type and extracts raw text."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
    elif ext == '.pdf':
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
                
    elif ext == '.docx':
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
            
    else:
        raise ValueError(f"Unsupported file format: {ext}. Use .txt, .pdf, or .docx")
        
    return text

# --- COMPONENT 2: Chunking Logic ---
def chunk_text(text, max_chars=500):
    """Slices a large document into smaller chunks."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        
        if current_length >= max_chars:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

# --- COMPONENT 3: Database Storage ---
def import_document(file_path):
    """Extracts, chunks, embeds, and saves the file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    file_name = os.path.basename(file_path)
    print(f"\n--- Processing {file_name} ---")

    # 1. Extract text dynamically based on file type
    try:
        raw_text = extract_text(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
        
    if not raw_text.strip():
        print("Error: Document is empty or could not be read.")
        return

    # 2. Chunk
    chunks = chunk_text(raw_text)
    print(f"Sliced document into {len(chunks)} chunks.")

    # 3. Connect to DB
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    # 4. Embed and Store
    for i, chunk_text_data in enumerate(chunks):
        embedding = model.encode(chunk_text_data).tolist()
        insert_query = """
            INSERT INTO docs (d_name, chunk_text, embedding) 
            VALUES (%s, %s, %s)
        """
        cur.execute(insert_query, (file_name, chunk_text_data, embedding))
        
    conn.commit()
    cur.close()
    conn.close()
    print("Import complete! Data is safe in PostgreSQL.")

# --- EXECUTION (Command Line Interface) ---
if __name__ == "__main__":
    # Check if the user provided a file path in the terminal
    if len(sys.argv) < 2:
        print("Usage: python import_docs.py <path_to_your_file>")
        print("Example: python import_docs.py C:/Users/Downloads/manual.pdf")
        sys.exit(1)
        
    target_file = sys.argv[1]
    import_document(target_file)