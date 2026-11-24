from fastapi import FastAPI, Header, HTTPException, Request
import os, traceback, time, logging
from groq import Groq
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("omniaforge")
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Too many requests - slow down, King"})
MY_KEY = "omnia-sk-123"
@app.get("/")
def home():
    return {"status":"OmniaForge live - auth + rate-limit + logging ready"}
@app.post("/generate")
@limiter.limit("10/minute")
def generate(request: Request, prompt: str = "hello", x_api_key: str = Header(None)):
    start = time.time()
    if x_api_key != MY_KEY:
        logger.warning(f"401 Unauthorized from {request.client.host}")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content": prompt}])
        output = chat.choices[0].message.content
        logger.info(f"200 OK | IP:{request.client.host} | prompt:{prompt[:50]} | time:{round(time.time()-start,2)}s")
        return {"output": output}
    except Exception as e:
        logger.error(f"500 Error: {e}")
        return {"error": str(e), "trace": traceback.format_exc()[:800]}
