from fastapi import FastAPI, Header, HTTPException
import os
from groq import Groq
app = FastAPI()
MY_KEY = "omnia-sk-123"
@app.get("/")
def home(): return {"status":"OmniaForge live - auth ready"}
@app.post("/generate")
def generate(prompt: str = "hello", x_api_key: str = Header(None)):
    if x_api_key != MY_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content": prompt}])
    return {"output": chat.choices[0].message.content}
