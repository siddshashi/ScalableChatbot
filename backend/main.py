import uvicorn
from fastapi import FastAPI, Header
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
collection.create_index("username") # index based on username

# Get the entire conversation for the user if it exists
@app.get("/queries", response_model=Queries)
def get_conversation(username: str = Header(..., alias="Username")):
    user_data = collection.find_one({"username": username}, {"_id": 0, "queries": 1})
    query_list = user_data["queries"] if user_data else []
    return Queries(queries=query_list)

# Handle user's question
@app.post("/queries", response_model=Query)
def add_query(query: Query, username: str = Header(..., alias="Username")):
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

    # Add to DB
    query_dict = query.dict()
    collection.update_one(
        {"username": username},
        {"$push": {"queries": query_dict}},
        upsert=True  # Creates a new document if user doesn't exist
    )
    return query

# Run and test API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)