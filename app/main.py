from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional

app = FastAPI()


client = MongoClient("mongodb://mongodb:27017/")
db = client.messages_db
collection = db.messages

class Message(BaseModel):
    content: str
    username: str

class MessageResponse(BaseModel):
    id: str
    content: str
    username: str

@app.get("/api/v1/messages/", response_model=List[MessageResponse])
def get_messages(skip: int = 0, limit: int = 10):
    messages = list(collection.find().skip(skip).limit(limit))
    response = []
    for message in messages:
        response.append(MessageResponse(id=str(message["_id"]), content=message["content"], username=message["username"]))
    return response

@app.post("/api/v1/message/")
def post_message(message: Message):
    message_id = collection.insert_one(message.dict()).inserted_id
    return {"id": str(message_id)}

@app.delete("/api/v1/messages/")
def delete_all_messages():
    result = collection.delete_many({})
    return {"deleted_count": result.deleted_count}