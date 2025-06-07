# Requires transformers>=4.51.0
# Requires sentence-transformers>=2.7.0

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the model
# model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# We recommend enabling flash_attention_2 for better acceleration and memory saving,
# together with setting `padding_side` to "left":
model = SentenceTransformer(
    "Qwen/Qwen3-Embedding-0.6B",
    # model_kwargs={"attn_implementation": "flash_attention_2", "device_map": "auto"},
    model_kwargs={"device_map": "auto"},
    tokenizer_kwargs={"padding_side": "left"},
)

# The queries and documents to embed
queries = [
    "What is the capital of China?",
    "Explain gravity",
]
documents = [
    "The capital of China is Beijing.",
    "Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun.",
]

# Encode the queries and documents. Note that queries benefit from using a prompt
# Here we use the prompt called "query" stored under `model.prompts`, but you can
# also pass your own prompt via the `prompt` argument
query_embeddings = model.encode(queries, prompt_name="query")
document_embeddings = model.encode(documents)

# Compute the (cosine) similarity between the query and document embeddings
similarity = model.similarity(query_embeddings, document_embeddings)
print(similarity)
# tensor([[0.7493, 0.0751],
#         [0.0880, 0.6318]])

# Create faiss index
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Normalize for cosine similarity
faiss.normalize_L2(document_embeddings)
index.add(document_embeddings)

faiss.normalize_L2(query_embeddings)
D, I = index.search(query_embeddings, k=2)

for idx in I[0]:
    print("match:", documents[idx])