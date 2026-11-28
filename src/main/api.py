from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from groq import Groq
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
MY_KEY = os.getenv("HEDRA_API_KEY")
@app.get("/")
def home():
    return {"status":"OmniaForge live - auth ready"}
@app.post("/generate")
def generate(prompt: str = "hello", x_api_key: str = Header(None)):
    if x_api_key != MY_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role":"user","content": prompt}]
    )
    return {"output": chat.choices[0].message.content}
