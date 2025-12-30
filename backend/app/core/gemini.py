import os
from google import genai
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Initialize Gemini client using API key from environment
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_text(prompt: str) -> str:
    """
    Generate text using Gemini model.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
def explain_build(build: dict, use_case: str) -> str:
    """
    Generate a human-readable explanation for a build.
    """

    components = build["components"]
    price = build["total_price"]
    strategy = build["strategy"]

    component_lines = []
    for part, item in components.items():
        component_lines.append(
            f"- {part.upper()}: {item['name']} (₹{item['price_inr']})"
        )

    prompt = f"""
You are an expert PC advisor.

Explain the following PC build for a {use_case} user.

Strategy: {strategy}
Total Price: ₹{price}

Components:
{chr(10).join(component_lines)}

Explain:
- Why this build fits the use case
- Key strengths
- Trade-offs
- Who should choose this build

Keep the explanation concise and beginner-friendly.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text