from sentence_transformers import SentenceTransformer
from pathlib import Path
import faiss
import numpy as np


# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_pc_part_texts() -> list[str]:
    """
    Load PC part descriptions from processed text file.
    Each line represents one PC part.
    """
    data_path = Path("backend/data/processed/pc_parts.txt")

    texts = []
    with open(data_path, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if clean_line:
                texts.append(clean_line)

    return texts

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text strings into embedding vectors.
    """
    return embedding_model.encode(texts, convert_to_numpy=True).tolist()


def generate_pc_part_embeddings():
    """
    Load PC part texts and generate embeddings for them.
    """
    texts = load_pc_part_texts()
    embeddings = generate_embeddings(texts)
    return texts, embeddings

def create_faiss_index(embeddings: list[list[float]]):
    """
    Create a FAISS index from embedding vectors.
    Uses cosine similarity.
    """
    # Convert embeddings to numpy array
    embedding_array = np.array(embeddings).astype("float32")

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embedding_array)

    # Create FAISS index
    dimension = embedding_array.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings to index
    index.add(embedding_array)

    return index

def save_faiss_index(index, index_path: str):
    """
    Save FAISS index to disk.
    """
    faiss.write_index(index, index_path)


def load_faiss_index(index_path: str):
    """
    Load FAISS index from disk.
    """
    return faiss.read_index(index_path)
