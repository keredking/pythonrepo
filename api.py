import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Serve /static/* files from the "static" folder
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    # Serves the website UI
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY not set"}

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Keep answers concise."},
            {"role": "user", "content": req.question},
        ],
        temperature=0.7,
    )

    answer = completion.choices[0].message.content
    return {"answer": answer}