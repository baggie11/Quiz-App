# import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Load environment variables
load_dotenv(override=True)

from bot_fast_api import run_bot
from bot_websocket_server import run_bot_websocket_server



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles FastAPI startup and shutdown."""
    # Startup
    print("Starting FastAPI server with question fetching from Node API")
    print(f"Node API URL: {os.getenv('NODE_API_URL', 'http://localhost:3000')}")
    yield  # Run app
    # Shutdown
    print("Shutting down FastAPI server")


# Initialize FastAPI app with lifespan manager
app = FastAPI(lifespan=lifespan)

# Configure CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: str = "H6TU"):
    await websocket.accept()
    print(f"🔗 WebSocket connection with session: {session}")  # ADD THIS LINE
    try:
        await run_bot(websocket, session)
    except Exception as e:
        print(f"Exception in run_bot: {e}")


@app.post("/connect")
async def bot_connect(request: Request):
    """Handle Pipecat client connection request"""
    try:
        data = await request.json()
        session_code = data.get("sessionCode", "H6TU")
        
        # Validate session
        if not session_code or len(session_code) < 3:
            session_code = "H6TU"
        
        print(f"📋 Client requesting connection with session: {session_code}")
        
        # Pipecat client expects EXACTLY this format:
        return {
            "ws_url": f"ws://localhost:7860/ws?session={session_code}"
        }
        
    except Exception as e:
        print(f"Error in /connect: {e}")
        return {"ws_url": "ws://localhost:7860/ws?session=H6TU"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pipecat-bot",
        "question_fetching": "enabled"
    }


async def main():
    server_mode = os.getenv("WEBSOCKET_SERVER", "fast_api")
    tasks = []
    try:
        if server_mode == "websocket_server":
            tasks.append(run_bot_websocket_server())

        config = uvicorn.Config(app, host="0.0.0.0", port=7860)
        server = uvicorn.Server(config)
        tasks.append(server.serve())

        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Tasks cancelled (probably due to shutdown).")


if __name__ == "__main__":
    asyncio.run(main())


