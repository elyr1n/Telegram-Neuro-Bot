import base64

from aiogram.types import Message
from app.database import get_context


def img_to_base64(image):
    return base64.b64encode(image.read()).decode("utf-8")


def get_context_from_user(message: Message, limit: int = 10):
    context_messages = get_context(message.from_user.id, limit)

    context_text = ""
    if context_messages:
        context_text = "Контекст диалога:\n"
        for role, content in context_messages:
            if role == "user":
                context_text += f"Пользователь: {content}\n"
            else:
                context_text += f"Ассистент: {content}\n"
        context_text += "\nТекущий запрос:\n"

    return context_text + message.text
