from main import ask_question
from config import Config

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(Config.API_TG)
dp = Dispatcher()
@dp.message(Command("start"))
async def start(message):
    welcome_text = """
👋 Привет! Я — AI-помощник по русскому языку для подготовки к ЕГЭ.

📚 Я умею:
• Отвечать на вопросы по русскому языку
• Объяснять правила и исключения
• Помогать с разбором сложных тем
• Давать структурированные ответы с указанием источников

⚠️ Важно: Я НЕ заменяю профессионального репетитора

❓ Как задать вопрос?
Просто напиши мне свой вопрос, и я постараюсь помочь!

Удачи в подготовке к ЕГЭ! 🍀
"""
    await message.answer(welcome_text)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = """
❓ Как пользоваться ботом:

1. Напиши вопрос по русскому языку
2. Я найду ответ в учебных материалах
3. Получишь структурированный ответ с источником

⚠️ Если я не знаю ответа — скажу честно.
"""
    await message.answer(help_text)

@dp.message()
async def handle_question(message):
    user_text = message.text
    await bot.send_chat_action(message.chat.id, action='typing')
    try:
        response = ask_question(user_text)
        await message.answer(response[:4096])
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте переформулировать вопрос или повторите позже.")
        print(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())