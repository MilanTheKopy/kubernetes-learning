from pydantic import BaseModel
import os
import asyncio
import httpx
import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI

AGENT_NAME = os.getenv("AGENT_NAME", "unknown-agent") #hier lesen wir umgebungsvariablen aus. diese werden 
TARGET_HOST = os.getenv("TARGET_HOST") #im deployment unter containers/env definiert, siehe alpha deployment
PORT = 50000

async def send_messages():
    await asyncio.sleep(5)

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.post(
                    f"http://{TARGET_HOST}:{PORT}/message",
                    json={
                        "sender": AGENT_NAME,
                        "message": f"Hello from {AGENT_NAME} at {datetime.datetime.now()}"
                    },
                    timeout=5
                )

                print(
                    f"[{AGENT_NAME}] response: {response.json()}",
                    flush=True
                )

            except Exception as e:
                print(
                    f"[AGENT_NAME: {AGENT_NAME},AGENT_NAME: {TARGET_HOST},AGENT_NAME: {PORT}] request failed: {e}",
                    flush=True
                )

            await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):

    asyncio.create_task(send_messages())
    print("server sollte nun gestartet werden")
    yield


app = FastAPI(lifespan=lifespan)

class Message(BaseModel):
    sender: str
    message: str

@app.post("/message")
def message(data: Message):
    print(f"{AGENT_NAME} received Message: {data}")
    return {"status":"ok"}






