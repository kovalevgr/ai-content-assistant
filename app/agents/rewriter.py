import os
import openai
from typing import Optional, List

openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 500))

async def rewrite_text(text: str, style: str = "professional", images: Optional[List[str]] = None) -> str:
    """
    Rewrite the given text in the specified style.
    Optionally, embed image references into the text if provided.

    :param text: The original text to rewrite
    :param style: The writing style ("professional", "casual", etc.)
    :param images: Optional list of image URLs to embed into the text
    :return: Rewritten text
    """
    if not text:
        return "No text provided for rewriting."

    prompt = (
        f"Rewrite the following text in a {style} style. "
        f"Make it engaging and natural. "
    )

    if images:
        prompt += (
            "Also, suggest where the following images can be embedded to enhance the article:\n"
        )
        for idx, img_url in enumerate(images, start=1):
            prompt += f"- [Image{idx}]: {img_url}\n"
        prompt += (
            "Insert [Image1], [Image2], etc., into appropriate places in the rewritten text.\n"
        )

    prompt += f"\nOriginal text:\n{text}"

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert article editor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        rewritten_text = response["choices"][0]["message"]["content"]
        return rewritten_text.strip()

    except Exception as e:
        print(f"Error rewriting text: {e}")
        return text