from app.core.embeddings import build_faiss_index
from app.core.rag_loader import load_rag_texts

VECTOR_INDEX_PATH = "backend/vector_store/rag_knowledge.faiss"


def build_rag_index():
    print("Loading RAG knowledge texts...")
    texts = load_rag_texts()

    print(f"Total RAG chunks: {len(texts)}")

    print("Building FAISS index...")
    build_faiss_index(texts, VECTOR_INDEX_PATH)

    print("RAG FAISS index built successfully.")


if __name__ == "__main__":
    build_rag_index()
