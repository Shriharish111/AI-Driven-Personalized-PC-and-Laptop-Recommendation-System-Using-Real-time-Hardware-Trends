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
