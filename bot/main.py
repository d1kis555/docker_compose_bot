import asyncio
from aiogram import Bot, Dispatcher, types
from motor.motor_asyncio import AsyncIOMotorClient

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

client = AsyncIOMotorClient('mongodb://mongodb:27017')
db = client.messages_db
collection = db.messages

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome! Use /messages to get messages or send a message to create one.")

@dp.message_handler(commands=['messages'])
async def get_messages(message: types.Message):
    messages = await collection.find().to_list(100)
    response = "\n".join([msg["content"] for msg in messages])
    await message.reply(response if response else "No messages.")

@dp.message_handler()
async def create_message(message: types.Message):
    await collection.insert_one({"content": message.text})
    await message.reply("Message saved!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())