# AI Agent Web Interface v2.0

Local-first, production-ready full-stack web interface for the 31-tool AI SysAdmin & DevSecOps Agent.

## Stack
- **Frontend**: React 18 + TypeScript + Vite + TailwindCSS + Zustand + Socket.IO-Client
- **Backend**: FastAPI + Python-SocketIO + SQLAlchemy + SQLite + OpenAI Stream Client
- **Tool Suite**: 31 native fully-authorized tools (Git, Docker, Shell, WinRM, K8s, DB, File System, Code Format/Patch)

## Quick Start (Docker)

```bash
docker-compose up --build
```
Access frontend at `http://localhost:3000` and backend API at `http://localhost:8000`.

## Local Development (Without Docker)

### Backend:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```
