import os

from dotenv import load_dotenv
from openai import AsyncOpenAI, BadRequestError, APIStatusError

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("AI"),
)


async def generate(prompt: str):
    try:
        completion = await client.chat.completions.create(
            model="deepseek/deepseek-chat",
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
