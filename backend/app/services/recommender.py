from app.core.rag import retrieve_relevant_parts
from app.core.gemini import generate_text


def generate_pc_recommendation(user_intent: str) -> str:
    """
    Generate a PC recommendation using RAG + Gemini.
    """
    # Step 1: Retrieve relevant hardware context
    retrieved_parts = retrieve_relevant_parts(user_intent, top_k=5)

    if not retrieved_parts:
        return "No relevant hardware data found for the given requirements."

    # Step 2: Format retrieved context
    context_block = "\n".join(
        f"- {part}" for part in retrieved_parts
    )

    # Step 3: Construct Gemini prompt
    prompt = f"""
You are a PC hardware expert.

Use ONLY the following hardware information to make recommendations.
Do NOT assume specifications that are not listed.
Do NOT mention brands or parts not present in the data.

HARDWARE DATA:
{context_block}

USER REQUIREMENT:
{user_intent}

TASK:
Recommend a suitable PC configuration.
Explain:
- Why these parts fit the requirement
- Trade-offs involved
- Performance expectations

Answer clearly and concisely.
"""

    # Step 4: Generate response using Gemini
    response = generate_text(prompt)

    return response
