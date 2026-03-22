# Telegram-Neuro-Bot

A Telegram bot that integrates with a neural network (via OpenRouter) to generate responses while maintaining chat context and providing admin moderation tools.

To test the bot, I launched it in my TG channel - @tg_neuronet_bot.

## Features

- Responds to user text messages using a neural network
- Maintains chat context (last 10 messages) for coherent conversations
- Admin commands for user banning/unbanning
- Context clearing for privacy or restart
- SQLite database for storing users, bans, and chat history
- Asynchronous operations for performance

## Commands

| Command | Description | Access |
|---------|-------------|--------|
| `/start` | Start the bot and register the user | All users |
| `/clear` | Clear the conversation context for the user | All users (except banned) |
| `/ban <user_id>` | Ban a user from using the bot | Admin only |
| `/unban <user_id>` | Unban a previously banned user | Admin only |

## Installation

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- OpenRouter API Key (from [openrouter.ai](https://openrouter.ai))

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/elyr1n/Telegram-Neuro-Bot.git
   cd Telegram-Neuro-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```env
   AI=your_openrouter_api_key
   TOKEN=your_telegram_bot_token
   CHAT_IDS=your_telegram_user_ids
   ```

4. Initialize the database:
   The database is automatically created when the bot starts.

5. Run the bot:
   ```bash
   python bot.py
   ```

## Configuration

The bot uses environment variables for configuration. Create a `.env` file with the following variables:

| Variable | Description |
|----------|-------------|
| `AI` | OpenRouter API key |
| `TOKEN` | Telegram bot token obtained from @BotFather |
| `CHAT_IDS` | Your Telegram user ID (for admin commands) |

## Project Structure

```
Telegram-Neuro-Bot/
├── app/
│   ├── __init__.py
│   ├── handlers.py      # Message handlers and commands
│   ├── generation.py    # Neural network integration
│   └── database.py      # SQLite database operations
├── bot.py               # Main bot entry point
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not tracked)
```

## Database Schema

- **users**: Stores user information (chat_id, name, username)
- **users_in_ban**: List of banned user IDs
- **chat_context**: Conversation history (chat_id, role, content, timestamp)

## Dependencies

- `aiogram` - Telegram Bot API framework
- `openai` - OpenRouter API client
- `python-dotenv` - Environment variable management

---

Телеграм-бот, интегрированный с нейросетью (через OpenRouter), который генерирует ответы, поддерживая контекст диалога и предоставляя инструменты модерации для администратора.

Для тестирования бота я запустил в ТГ своего - @tg_neuronet_bot.

## Возможности

- Отвечает на текстовые сообщения пользователей с помощью нейросети
- Поддерживает контекст диалога (последние 10 сообщений) для связных бесед
- Команды администратора для блокировки/разблокировки пользователей
- Очистка контекста для конфиденциальности или перезапуска
- SQLite база данных для хранения пользователей, блокировок и истории сообщений
- Асинхронная работа для высокой производительности

## Команды

| Команда | Описание | Доступ |
|---------|----------|--------|
| `/start` | Запуск бота и регистрация пользователя | Все пользователи |
| `/clear` | Очистка контекста диалога для пользователя | Все пользователи (кроме заблокированных) |
| `/ban <user_id>` | Заблокировать пользователя | Только администратор |
| `/unban <user_id>` | Разблокировать пользователя | Только администратор |

## Установка

### Требования
- Python 3.8+
- Токен Телеграм бота (от [@BotFather](https://t.me/BotFather))
- API ключ OpenRouter (от [openrouter.ai](https://openrouter.ai))

### Шаги

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/elyr1n/Telegram-Neuro-Bot.git
   cd Telegram-Neuro-Bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корне проекта:
   ```env
   AI=ваш_api_ключ_openrouter
   TOKEN=ваш_токен_телеграм_бота
   CHAT_IDS=ваши_id_в_телеграм
   ```

4. База данных создастся автоматически при первом запуске бота.

5. Запустите бота:
   ```bash
   python bot.py
   ```

## Конфигурация

Бот использует переменные окружения для настройки. Создайте файл `.env` со следующими переменными:

| Переменная | Описание |
|------------|----------|
| `AI` | API ключ OpenRouter |
| `TOKEN` | Токен Телеграм бота от @BotFather |
| `CHAT_IDS` | Ваш ID пользователя в Телеграм (для команд администратора) |

## Структура проекта

```
Telegram-Neuro-Bot/
├── app/
│   ├── __init__.py
│   ├── handlers.py      # Обработчики сообщений и команд
│   ├── generation.py    # Интеграция с нейросетью
│   └── database.py      # Работа с базой данных SQLite
├── bot.py               # Главный файл запуска бота
├── requirements.txt     # Зависимости Python
└── .env                 # Переменные окружения (не в репозитории)
```

## Схема базы данных

- **users**: информация о пользователях (chat_id, имя, username)
- **users_in_ban**: список заблокированных пользователей
- **chat_context**: история диалога (chat_id, роль, текст, время)

## Зависимости

- `aiogram` - фреймворк для работы с Telegram Bot API
- `openai` - клиент для OpenRouter API
- `python-dotenv` - управление переменными окружения
