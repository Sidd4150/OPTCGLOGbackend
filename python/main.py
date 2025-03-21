
import database
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://onepiecetcglog-production.up.railway.app/"],  # Allow all origins (for development, specify your frontend URL like "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class DataInput(BaseModel): 
    name: str
    img: str
    setName: str
    price: float
    groupID: int

@app.get("/api/data")
async def get_data(data: DataInput):
    # Log the received data
    print(f"Received data: {data}")
    
    # Respond with a JSON response
    return JSONResponse(content={"message": "Data received successfully PythonBack", "receivedData": {data}})

@app.get("/api/filter")
async def filter_cards(filter: str = None):
    return database.filterDataBase(filter)

@app.get("/api/search")
async def filter_cards(filter: str = None):
    return database.filterDataBase(filter)

@app.get("/api/cards")
async def get_cards():
   return database.getCardsDataBase()