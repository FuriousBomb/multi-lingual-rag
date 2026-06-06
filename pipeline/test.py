from sentence_transformers import SentenceTransformer

# 1. Initialize the model (This will download a few hundred MBs the first time you run it)
print("Loading model...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. Create some sample text (English and Malayalam)
sample_texts = [
    "Employees must submit their timesheets by Friday at 5 PM.",
    "ജീവനക്കാർ വെള്ളിയാഴ്ച വൈകുന്നേരം 5 മണിക്ക് മുമ്പായി ടൈംഷീറ്റുകൾ സമർപ്പിക്കണം."
]

# 3. Generate the embeddings
print("Generating vectors...")
embeddings = model.encode(sample_texts)

# 4. Verify the output
for i, text in enumerate(sample_texts):
    print(f"\nText: {text}")
    print(f"Vector Dimensions: {len(embeddings[i])}")
    print(f"First 5 values: {embeddings[i][:5]}")