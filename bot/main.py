import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
from motor.motor_asyncio import AsyncIOMotorClient

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

if not API_TOKEN:
    raise ValueError("No TELEGRAM_API_TOKEN provided")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

client = AsyncIOMotorClient('mongodb://mongodb:27017')
db = client.messages_db
collection = db.messages

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Welcome! Use /messages to get messages or send a message to create one.")

@dp.message(Command("messages"))
async def get_messages(message: types.Message):
    messages = await collection.find().to_list(100)
    response = "\n".join([f"{msg.get('username', 'Unknown User')}: {msg.get('content', 'No Content')}" for msg in messages])
    await message.reply(response if response else "No messages.")

@dp.message(Command("clear"))
async def clear_messages(message: types.Message):
    result = await collection.delete_many({})
    count = result.deleted_count
    await message.reply(f"All messages have been deleted. {count} message(s) removed.")

@dp.message()
async def create_message(message: types.Message):
    user = message.from_user
    message_data = {
        "username": user.username or user.full_name,  
        "content": message.text
    }
    await collection.insert_one(message_data)
    await message.reply("Message saved!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())