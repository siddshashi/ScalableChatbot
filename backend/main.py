import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Query(BaseModel):
    question: str
    # response: str

class Queries(BaseModel):
    queries: List[Query]

app = FastAPI()

# After deployment, add real production URL 
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # can send JWT tokens
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"queries": []} # simple, in memory database, non-persistent

# get the entire conversation
@app.get("/queries", response_model=Queries)
def get_conversation():
    return Queries(queries=memory_db["queries"])

# add a query to the db
@app.post("/queries", response_model=Query)
def add_query(query: Query):
    memory_db["queries"].append(query)
    return query

# run and test API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)