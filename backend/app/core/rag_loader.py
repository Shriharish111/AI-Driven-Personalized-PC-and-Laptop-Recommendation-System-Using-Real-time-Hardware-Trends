from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
RAG_DATA_DIR = BASE_DIR / "backend" / "data" / "rag"


def load_rag_texts() -> list[str]:
    """
    Load all RAG knowledge paragraphs from data/rag/*.txt
    Each paragraph becomes one retrievable chunk.
    """
    texts = []

    for file_path in RAG_DATA_DIR.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            # Split into paragraphs
            for paragraph in content.split("\n\n"):
                paragraph = paragraph.strip()
                if paragraph:
                    texts.append(paragraph)

    return texts
