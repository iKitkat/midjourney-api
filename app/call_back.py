import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class User(BaseModel):
    user: str

@app.post("/four_kids")
async def index(user: User):
   return user

if __name__ == "__main__":
   uvicorn.run("call_back:app", host="127.0.0.1", port=8024, reload=True)
