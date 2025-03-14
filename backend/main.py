import uvicorn
import json
import requests
import pymongo
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

OLLAMA_URL = "http://34.170.52.92/api/generate" 
MODEL_NAME = "mistral"
MONGO_DB_URL = "mongodb://162.222.183.206:27017" 

# Initialize MongoDB client
client = pymongo.MongoClient(MONGO_DB_URL)
db = client["history"]
collection = db["queries"] 

# Ensure index based on username for fast lookups
collection.create_index("username") 

# FastAPI app instance
app = FastAPI()

# CORS Configuration
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

# Pydantic Models
class Query(BaseModel):
    question: str
    response: str = None # Store response from Ollama

class Queries(BaseModel):
    queries: List[Query]

# Routes
@app.get("/queries", response_model=Queries)
def get_conversation(username: str = Header(..., alias="Username")):
    """
    Retrieve the entire conversation history for a specific user.
    The username is sent as a header.
    """
    user_data = collection.find_one({"username": username}, {"_id": 0, "queries": 1})
    query_list = user_data["queries"] if user_data else []
    return Queries(queries=query_list)

# Handle user's question
@app.post("/queries", response_model=Query)
def add_query(query: Query, username: str = Header(..., alias="Username")):
    """
    Process a user's query, send it to Ollama for a response,
    store it in MongoDB, and return the response.
    """
    # Send question to Ollama
    payload = {
        "model": MODEL_NAME,
        "prompt": query.question,
        "stream": False
    }

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

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)