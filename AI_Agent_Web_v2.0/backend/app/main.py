from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.core.config import settings
from app.api.routes import sessions, tools
from app.core.websocket_manager import sio_app, sio

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Agent Web Backend",
    version="2.0.0"
)

origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)
app.include_router(tools.router)

app.mount("/ws", sio_app)


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.on("chat:message")
async def handle_chat_message(sid, data):
    session_id = data.get("sessionId")
    content = data.get("content", "")

    # Emit typing / token stream
    await sio.emit("chat:token", "AI Ajanı (Web UI) isteğinizi işliyor: ", room=sid)
    await sio.emit("chat:token", content, room=sid)

    # Emit tool call simulation for demo / verification
    await sio.emit("chat:tool_call", {
        "id": "tc-101",
        "name": "list_directory",
        "arguments": {"path": "."}
    }, room=sid)

    await sio.emit("chat:tool_result", {
        "callId": "tc-101",
        "result": "Dizin içeriği: ['main.py', 'src', 'tests', 'AI_Agent_Web_v2.0']"
    }, room=sid)

    await sio.emit("chat:done", {}, room=sid)
