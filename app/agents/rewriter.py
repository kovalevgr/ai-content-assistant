import os
from openai import AsyncOpenAI
from typing import Optional, List

from dotenv import load_dotenv
load_dotenv()

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 500))

MAX_INPUT_WORDS = 500

def truncate_text(text: str, max_words: int) -> str:
    return ' '.join(text.split()[:max_words])

async def rewrite_text(text: str, style: str = "professional", images: Optional[List[str]] = None) -> str:
    """
    Rewrite text in a specific style, optionally embedding image markers.

    :param text: Original input
    :param style: Desired writing style
    :param images: List of image URLs to reference
    :return: Rewritten article
    """

    if not text:
        return "No text provided."

    truncated_text = truncate_text(text, MAX_INPUT_WORDS)

    prompt = (
        f"Rewrite the following text in a {style} style. "
        f"Keep it natural and easy to read.\n\n"
    )

    if images:
        prompt += (
            "Insert placeholders like [Image1], [Image2] at appropriate places in the text "
            "to indicate where images could be shown. Here are the images:\n"
        )
        for i, url in enumerate(images, start=1):
            prompt += f"[Image{i}]: {url}\n"

    prompt += f"\nOriginal:\n{truncated_text}"

    try:
        response = await aclient.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful and creative article editor."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Rewrite error: {e}")
        return text