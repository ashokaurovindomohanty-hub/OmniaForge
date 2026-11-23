from fastapi import FastAPI
import os
app = FastAPI()
@app.get("/")
def home(): return {"status":"OmniaForge live - LLM ready"}
@app.post("/generate")
def generate(prompt: str = "hello"):
    # placeholder - will call LLM
    try:
        # if GROQ_API_KEY set, use it
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content": prompt}]
        )
        return {"output": chat.choices[0].message.content}
    except Exception as e:
        return {"output": f"Generated for: {prompt} (set GROQ_API_KEY for AI) - {e}"}
print("api updated")
