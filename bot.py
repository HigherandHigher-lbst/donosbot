import asyncio
from aiogram import Bot, Dispatcher, types, F

const express = require('express')
const app = express()
const port = process.env.PORT || 4000

TOKEN = "8225110405:AAE6PO-F3GVDxRzbd2LJqUTBLaxcpLY2BXw"
GROUP_ID = "@shlakoCHAT"
TOPIC_ID = 11
MY_ID = 5110146436


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Привет! Хочешь написать донос? (за фейк будет варн)")

@dp.message(F.text)
async def handle_report(message: types.Message):
    if message.chat.type == 'private':
        try:
            
            await bot.send_message(
                chat_id=GROUP_ID, 
                text=f"📢 **Анонимный донос:**\n\n{message.text}",
                message_thread_id=TOPIC_ID
            )
            
            user = message.from_user
            info = f"👤 От: {user.full_name} (@{user.username})\nID: {user.id}\nТекст: {message.text}"
            await bot.send_message(MY_ID, info)
            
            
            await message.answer("Спасибо за ваш донос!")
        except Exception as e:
            print(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
