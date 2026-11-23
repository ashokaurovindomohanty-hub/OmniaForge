from fastapi import FastAPI
import os
app = FastAPI()
@app.get("/")
def home(): return {"status":"OmniaForge live - LLM ready"}
@app.post("/generate")
def generate(prompt: str = "hello"):
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role":"user","content": prompt}]
    )
    return {"output": chat.choices[0].message.content}
print("fixed gpt-oss")
