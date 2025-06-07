import os
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

# 1. Load Qwen3 model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# 2. Prepare your documents and queries
documents = [
    "The capital of China is Beijing.",
    "Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun.",
]
doc_embeddings = model.encode(documents)

# 3. Setup ChromaDB
chromadb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".chroma")
chroma_client = chromadb.PersistentClient(path=chromadb_path)
collection = chroma_client.get_or_create_collection(name="my_collection")

# 4. Add documents with embeddings
collection.upsert(
    documents=documents,
    embeddings=doc_embeddings.tolist(),  # Chroma expects a list of lists
    ids=["id1", "id2"]
)

# 5. Query: encode with Qwen3, then search
# query = "What is the capital of China?"
query = "Explain gravity"
query_embedding = model.encode([query])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=2
)
print(results)

best_idx = 0  # first result is the closest match
best_id = results['ids'][0][best_idx]
best_doc = results['documents'][0][best_idx]
best_distance = results['distances'][0][best_idx]

print("Best match ID:", best_id)
print("Best match document:", best_doc)
print("Distance:", best_distance)