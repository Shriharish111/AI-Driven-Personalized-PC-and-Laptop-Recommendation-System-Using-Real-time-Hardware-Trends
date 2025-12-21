from app.core.embeddings import (
    generate_pc_part_embeddings,
    create_faiss_index,
    save_faiss_index,
)



def build_vector_store():
    print("Loading PC part texts and generating embeddings...")
    texts, embeddings = generate_pc_part_embeddings()

    print("Creating FAISS index...")
    index = create_faiss_index(embeddings)

    print("Saving FAISS index to disk...")
    save_faiss_index(index)


    print("Vector store built successfully!")


if __name__ == "__main__":
    build_vector_store()
