import os

from dotenv import load_dotenv
from openai import AsyncOpenAI, BadRequestError, APIStatusError

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1/",
    api_key=os.getenv("AI"),
)


async def generate_image_neuro(prompt: str, image: str):
    try:
        completion = await client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Пиши свой ответ без какого-либо форматирования {prompt}"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                        },
                    ],
                }
            ],
        )
        return completion.choices[0].message.content

    except (BadRequestError, APIStatusError) as e:
        return f"Ошибка запроса: {e}"


async def generate_text_neuro(prompt: str):
    try:
        completion = await client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return completion.choices[0].message.content

    except (BadRequestError, APIStatusError) as e:
        return f"Ошибка запроса: {e}"
