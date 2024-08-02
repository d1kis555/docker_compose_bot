from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

client = AsyncIOMotorClient('mongodb://mongodb:27017')
db = client.messages_db
collection = db.messages

class Message(BaseModel):
    content: str

@app.get("/api/v1/messages/")
async def get_messages():
    messages = await collection.find().to_list(1000)
    return [{"id": str(msg["_id"]), "content": msg["content"]} for msg in messages]

@app.post("/api/v1/message/")
async def create_message(message: Message):
    result = await collection.insert_one(message.dict())
    return {"id": str(result.inserted_id)}