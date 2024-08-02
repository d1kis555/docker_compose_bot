from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List

app = FastAPI()

client = AsyncIOMotorClient('mongodb://mongodb:27017')
db = client.messages_db
collection = db.messages

class Message(BaseModel):
    username: str
    content: str

class MessageCreate(BaseModel):
    username: str
    content: str

@app.get("/api/v1/messages/", response_model=List[Message])
async def get_messages():
    messages = await collection.find().to_list(100)
    return messages

@app.post("/api/v1/message/")
async def create_message(message: MessageCreate):
    message_data = message.dict()
    result = await collection.insert_one(message_data)
    if result.inserted_id:
        return {"message": "Message saved successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to save message")