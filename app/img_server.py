from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

db_dir = "/root/img_db/"
app = FastAPI()

@app.get("/img/{img_id}")
async def main(img_id):
    return FileResponse(db_dir+img_id+".jpg")

if __name__ == "__main__":
    uvicorn.run("img_server:app", host="127.0.0.1", port=8024, reload=True)

