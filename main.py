from fastapi import FastAPI
from websocket import websocket_endpoint
from dotenv import load_dotenv
import os

load_dotenv()

PORT = os.getenv("PORT", 10000)

app = FastAPI()

# Register the WebSocket route
app.websocket("/ws")(websocket_endpoint)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
