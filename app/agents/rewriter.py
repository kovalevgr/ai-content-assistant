import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 500))

async def rewrite_text(text: str, style: str = "professional") -> str:
    """Rewrite given text into a specific writing style."""
    if not text:
        return "No text provided for rewriting."

    prompt = (
        f"Rewrite the following text in a {style} style:\n\n"
        f"{text}"
    )

    response = await openai.ChatCompletion.acreate(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional writer assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=OPENAI_TEMPERATURE,
        max_tokens=OPENAI_MAX_TOKENS,
    )

    return response['choices'][0]['message']['content'].strip()