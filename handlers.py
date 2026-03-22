import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generation import generate
from app.database import (
    add_user,
    is_user_banned,
    ban_user,
    unban_user,
    add_to_context,
    get_context,
    clear_context,
)

from dotenv import load_dotenv

load_dotenv()

router = Router()


class Generate(StatesGroup):
    text = State()


ADMIN_CHAT_IDS = [int(id) for id in os.getenv("CHAT_IDS").split(", ")]


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    add_user(
        chat_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
    )

    await message.answer(
        f"Приветствую, *{user.first_name}*!\n\n"
        "Это *бот*, с помощью которого *можно отправлять запросы в нейросеть*.\n\n"
        "Напиши свой *запрос текстом*, чтобы я на него ответил!",
        parse_mode="Markdown",
    )


@router.message(Generate.text)
async def generate_text_error(message: Message):
    await message.answer(
        "*Вы уже ввели запрос*. Пожалуйста, *подождите, перед тем как он выполнится*!",
        parse_mode="Markdown",
    )


@router.message(Command("ban"))
async def ban_user_command(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_CHAT_IDS:
        await message.answer(
            "*У вас нет прав для блокировки пользователей.*", parse_mode="Markdown"
        )
        return

    try:
        target_id = int(message.text.split()[1])
    except IndexError:
        await message.answer(
            "*Укажите ID пользователя для блокировки.*", parse_mode="Markdown"
        )
        return
    except ValueError:
        await message.answer(
            "*Неверный формат ID пользователя.*", parse_mode="Markdown"
        )
        return

    if user_id == target_id:
        await message.answer(
            "*Вы не можете заблокировать себя.*", parse_mode="Markdown"
        )
        return

    ban_user(target_id)
    clear_context(target_id)

    await message.answer(
        f"*Пользователь* с ID {target_id} *заблокирован*.", parse_mode="Markdown"
    )


@router.message(Command("unban"))
async def unban_user_command(message: Message):
    user_id = message.from_user.id
    if user_id not in ADMIN_CHAT_IDS:
        await message.answer(
            "*У вас нет прав для разблокировки пользователей.*", parse_mode="Markdown"
        )
        return

    try:
        target_id = int(message.text.split()[1])
    except IndexError:
        await message.answer(
            "*Укажите ID пользователя для разблокировки.*", parse_mode="Markdown"
        )
        return
    except ValueError:
        await message.answer(
            "*Неверный формат ID пользователя.*", parse_mode="Markdown"
        )
        return

    unban_user(target_id)

    await message.answer(
        f"*Пользователь* с ID {target_id} *разблокирован*.", parse_mode="Markdown"
    )


@router.message(Command("clear"))
async def clear_context_command(message: Message):
    if is_user_banned(message.from_user.id):
        await message.answer(
            "*Вы заблокированы и не можете использовать этого бота.*",
            parse_mode="Markdown",
        )
        return

    clear_context(message.from_user.id)
    await message.answer(
        "*Контекст диалога очищен!* Теперь я не помню предыдущие сообщения.",
        parse_mode="Markdown",
    )


@router.message(F.text)
async def generate_text(message: Message, state: FSMContext):
    if is_user_banned(message.from_user.id):
        await message.answer(
            "*Вы заблокированы и не можете использовать этого бота.*",
            parse_mode="Markdown",
        )
        return False

    await state.set_state(Generate.text)

    loading_message = await message.answer(
        "*Генерируется ответ...*", parse_mode="Markdown"
    )

    add_to_context(message.from_user.id, "user", message.text)

    context_messages = get_context(message.from_user.id, limit=10)

    context_text = ""
    if context_messages:
        context_text = "Контекст диалога:\n"
        for role, content in context_messages:
            if role == "user":
                context_text += f"Пользователь: {content}\n"
            else:
                context_text += f"Ассистент: {content}\n"
        context_text += "\nТекущий запрос:\n"

    full_prompt = context_text + message.text

    response = await generate(full_prompt)

    add_to_context(message.from_user.id, "assistant", response)

    await loading_message.delete()
    await message.answer(response, parse_mode="Markdown")

    await state.clear()
