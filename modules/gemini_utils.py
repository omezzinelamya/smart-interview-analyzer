import os
from sentence_transformers import SentenceTransformer

# Load the model once (do this globally)
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """
    Embed text into a vector using sentence-transformers.
    Returns a list of floats.
    """
    embedding = model.encode(text)
    return embedding.tolist()