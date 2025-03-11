import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
import json
import pymongo

OLLAMA_URL = "http://localhost:11434/api/generate" # After deployment, add real production URL 
MODEL_NAME = "mistral"
MONGO_DB_URL = "mongodb://localhost:27017/" # After deployment, add real production URL

class Query(BaseModel):
    username: str
    question: str
    response: str = None # Store response from Ollama

class Queries(BaseModel):
    queries: List[Query]

app = FastAPI()

origins = [
    "http://localhost:5173" # After deployment, add real production URL 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Can send JWT tokens
    allow_methods=["*"],
    allow_headers=["*"],
)

headers = {
    "Content-Type": "application/json"
}

client = pymongo.MongoClient(MONGO_DB_URL)
db = client["history"]
collection = db["queries"]

# Get the entire conversation
@app.get("/queries", response_model=Queries)
def get_conversation():
    query_list = [Query(**doc) for doc in collection.find({}, {"_id": 0})]
    return Queries(queries=query_list)

# Add a query to the db
@app.post("/queries", response_model=Query)
def add_query(query: Query):
    # Send question to Ollama
    payload = {
        "model": MODEL_NAME,
        "prompt": query.question,
        "stream": False
    }

    # TODO: change naming, lots of things called "response"
    # TODO: implement graceful timeout handling
    response =requests.post(OLLAMA_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        query.response = actual_response
    else:
        query.response = "Error communicating with Ollama."

    collection.insert_one(query.dict()) # TODO: is dictionary conversion slow? 
    return query

# run and test API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)