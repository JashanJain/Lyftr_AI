from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from app.models import init_db
from app.storage import insert_message, list_messages, get_stats
from app.config import WEBHOOK_SECRET
import hmac, hashlib

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

class Message(BaseModel):
    message_id: str = Field(..., min_length=1)
    from_: str = Field(..., alias="from")
    to: str
    ts: str
    text: str | None = None

def verify_signature(body: bytes, signature: str):
    expected = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhook")
async def webhook(req: Request):
    body = await req.body()
    sig = req.headers.get("X-Signature")
    if not sig or not verify_signature(body, sig):
        raise HTTPException(401, "invalid signature")
    data = await req.json()
    insert_message(data)
    return {"status": "ok"}

@app.get("/messages")
def messages(limit:int=50, offset:int=0):
    return list_messages(limit, offset)

@app.get("/stats")
def stats():
    return get_stats()

@app.get("/health/live")
def live(): return {"status":"ok"}

@app.get("/health/ready")
def ready():
    if not WEBHOOK_SECRET:
        raise HTTPException(503)
    return {"status":"ok"}
