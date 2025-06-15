from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    if not message:
        return {"error": "No message provided"}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful customer service agent."},
            {"role": "user", "content": message}
        ]
    )
    return {"response": response['choices'][0]['message']['content']}
