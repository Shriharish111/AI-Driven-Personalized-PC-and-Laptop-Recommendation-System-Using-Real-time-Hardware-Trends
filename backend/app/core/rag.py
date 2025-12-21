import numpy as np
import faiss

from app.core.embeddings import (
    generate_embeddings,
    load_faiss_index,
    load_pc_part_texts,
)





def retrieve_relevant_parts(user_query: str, top_k: int = 5) -> list[str]:
    """
    Retrieve top-k relevant PC part descriptions for a given user query.
    """
    # Load FAISS index
    index = load_faiss_index()

    # Load original PC part texts
    pc_part_texts = load_pc_part_texts()

    # Generate embedding for user query
    query_embedding = generate_embeddings([user_query])
    query_vector = np.array(query_embedding).astype("float32")

    # Normalize query vector for cosine similarity
    faiss.normalize_L2(query_vector)

    # Perform similarity search
    distances, indices = index.search(query_vector, top_k)

    # Map indices to PC part texts
    retrieved_texts = []
    for idx in indices[0]:
        if idx < len(pc_part_texts):
            retrieved_texts.append(pc_part_texts[idx])

    return retrieved_texts
