from fastapi import FastAPI, File, UploadFile
from typing import List
import time
import asyncio
import ocr
import util

app = FastAPI()

#default route
@app.get("/")
def home():
    return {"message": "Visit the endpoint: /api/v1/extract_text to perform OCR."}

#post to extract text
@app.post("/api/v1/extract_text")
async def extract_text(Images: List[UploadFile] = File(...)):
    response = {}
    s = time.time()
    tasks = []
    for img in Images:
        print("Images Uploaded: ", img.filename)
        temp_file = util._save_file_to_server(img, path="./", save_as=img.filename)
        tasks.append(asyncio.create_task(ocr.read_image(temp_file)))
    text = await asyncio.gather(*tasks)
    for i in range(len(text)):
        response[Images[i].filename] = text[i]
    response["Time Taken"] = round((time.time() - s),2)

    return response