from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home(): return {"status":"OmniaForge live"}
@app.post("/generate")
def generate(prompt: str = "hello"): return {"output": f"Generated for: {prompt}"}
!cat /content/OmniaForge/src/main/api.py
