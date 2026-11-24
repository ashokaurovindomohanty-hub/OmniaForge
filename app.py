from fastapi import FastAPI, Header, HTTPException, Request
import os, traceback
from groq import Groq
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Too many requests - slow down, King"})
MY_KEY = "omnia-sk-123"
@app.get("/")
def home():
    return {"status":"OmniaForge live - auth + rate-limit ready"}
@app.post("/generate")
@limiter.limit("10/minute")
def generate(request: Request, prompt: str = "hello", x_api_key: str = Header(None)):
    if x_api_key != MY_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content": prompt}])
        return {"output": chat.choices[0].message.content}
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()[:800]}
