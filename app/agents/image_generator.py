import os
import openai
from typing import List

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_images(topic: str, num_images: int = 1, size: str = "1024x1024") -> List[str]:
    """
    Generate relevant images based on a given topic.

    :param topic: The topic for image generation (e.g., "AI Trends in .NET")
    :param num_images: Number of images to generate
    :param size: Size of the images (256x256, 512x512, 1024x1024)
    :return: List of URLs of the generated images
    """
    try:
        response = await openai.Image.acreate(
            prompt=f"Create an illustration or diagram related to: {topic}",
            n=num_images,
            size=size,
            model="dall-e-3"  # fallback to "dall-e-2" if necessary
        )

        image_urls = [item["url"] for item in response["data"]]
        return image_urls

    except Exception as e:
        print(f"Error generating images: {e}")
        return []