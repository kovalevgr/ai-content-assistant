import os
from openai import AsyncOpenAI

from dotenv import load_dotenv
load_dotenv()

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 500))

async def summarize_articles(articles: list) -> str:
    """Summarize multiple articles into a short, coherent and engaging article."""
    if not articles:
        return "No articles provided for summarization."

    combined_text = ""

    for article in articles:
        combined_text += f"Title: {article.get('title', '')}\nSummary: {article.get('summary', '')}\n\n"

    prompt = (
        "You are an assistant that creates professional, short news articles from multiple raw articles.\n\n"
        f"Summarize the following information into a clear, concise, and engaging article:\n\n{combined_text}"
    )

    response = await aclient.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional news summarizer."},
            {"role": "user", "content": prompt},
        ],
        temperature=OPENAI_TEMPERATURE,
        max_tokens=OPENAI_MAX_TOKENS,
    )

    return response.choices[0].message.content.strip()