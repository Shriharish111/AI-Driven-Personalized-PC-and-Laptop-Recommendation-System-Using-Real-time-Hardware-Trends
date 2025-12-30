from app.core.embeddings import embed_text, load_faiss_index

VECTOR_INDEX_PATH = "backend/vector_store/rag_knowledge.faiss"


def retrieve_relevant_parts(user_intent: str, top_k: int = 5) -> list[str]:
    """
    Retrieve relevant hardware knowledge using RAG.
    """
    query_embedding = embed_text(user_intent)

    index, texts = load_faiss_index(VECTOR_INDEX_PATH)

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(texts):
            results.append(texts[idx])

    return results
