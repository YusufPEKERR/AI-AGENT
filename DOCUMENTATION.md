# OpenPlexus AI SysAdmin & DevSecOps Agent - Documentation v2.0

## 📖 Overview

**OpenPlexus** is an open-source AI-powered System Administration and DevSecOps agent developed by **Yusuf PEKER**. It provides a web-based interface for managing servers, performing security audits, scanning vulnerabilities, and automating DevOps tasks through natural language interactions.

**Repository**: https://github.com/YusufPEKERR/AI-AGENT

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │  Chat   │  │ Tools   │  │ Monitor │  │Workspace│  │ Widgets  │
│  │Interface│  │Catalog  │  │ System  │  │Explorer │  │Dashboard │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │            │            │            │            │        │
│       └────────────┴─────┬───────┴────────────┴────────────┘        │
│                          ▼                                           │
│              ┌─────────────────────┐                                │
│              │   Zustand Store     │                                │
│              │  (Global State)     │                                │
│              └──────────┬──────────┘                                │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  Socket.IO Client   │◄──── WebSocket ────┐           │
│              │  (Real-time comm)   │                     │           │
│              └─────────────────────┘                     │           │
└─────────────────────────────────────────────────────────┼───────────┘
                                                          │
                                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Socket.IO  │  │   REST API  │  │   LLM       │             │
│  │  Server     │  │  (Sessions, │  │   Client    │             │
│  │  (WS)       │  │   Tools,    │  │   (Nemotron)│             │
│  └──────┬──────┘  │   System)   │  └──────┬──────┘             │
│         │         └──────┬──────┘         │                    │
│         └────────────────┼────────────────┘                    │
│                          ▼                                     │
│              ┌─────────────────────┐                            │
│              │   Tool Registry     │                            │
│              │  (100+ SysAdmin/    │                            │
│              │   DevSecOps Tools)  │                            │
│              └──────────┬──────────┘                            │
│                         ▼                                       │
│              ┌─────────────────────┐                            │
│              │   SQLite Database   │                            │
│              │  (Sessions, Msgs,   │                            │
│              │   Tool Calls)       │                            │
│              └─────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2 | UI Framework |
| TypeScript | 5.2 | Type Safety |
| Vite | 5.2 | Build Tool |
| TailwindCSS | 3.4 | Styling |
| Zustand | 4.5 | State Management |
| Socket.IO Client | 4.7 | Real-time Communication |
| Lucide React | 0.368 | Icons |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.110 | Web Framework |
| Python | 3.12 | Runtime |
| python-socketio | 5.11 | WebSocket Server |
| SQLAlchemy | 2.0 | ORM |
| aiosqlite | 0.20 | Async SQLite Driver |
| OpenAI Python | 1.30 | LLM Client (NVIDIA API) |
| Pydantic | 2.7 | Validation |
| Uvicorn | 0.29 | ASGI Server |

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+
- **Python** 3.11+
- **Docker** (optional)

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/YusufPEKERR/AI-AGENT.git
cd AI-AGENT

# Configure environment
cp AI_Agent_Web_v2.0/backend/.env.example AI_Agent_Web_v2.0/backend/.env
# Edit .env with your NVIDIA API key

# Start services
docker-compose up -d --build

# Access frontend: http://localhost:3000
# Access backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Development Setup

#### Backend
```bash
cd AI_Agent_Web_v2.0/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your NVIDIA API key

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd AI_Agent_Web_v2.0/frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Access: http://localhost:3000
```

---

## ⚙️ Configuration

### Backend Environment Variables (`backend/.env`)

```env
# Database
DATABASE_URL=sqlite:///./app_data.db

# LLM Configuration (NVIDIA Nemotron 3 Ultra)
OPENAI_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL_NAME=nvidia/nemotron-3-ultra-550b-a55b

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Environment (Vite)

Create `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_URL=http://localhost:8000
```

---

## 📡 API Reference

### REST Endpoints

#### Sessions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sessions` | List all chat sessions |
| POST | `/api/sessions` | Create new session |
| GET | `/api/sessions/{id}` | Get session details |
| PUT | `/api/sessions/{id}` | Update session title |
| DELETE | `/api/sessions/{id}` | Delete session |
| GET | `/api/sessions/{id}/messages` | Get session messages |

#### Tools
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tools` | List all available tools |
| GET | `/api/tools/categories` | List tool categories |
| POST | `/api/tools/execute` | Execute a tool directly |

#### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/system/metrics` | Get system metrics |
| GET | `/api/system/health` | Health check |
| GET | `/api/workspace/tree` | Get workspace file tree |
| GET | `/api/workspace/file` | Read file content |
| POST | `/api/workspace/file` | Write file content |

### WebSocket Events (Socket.IO)

**Connection**: `ws://localhost:8000/ws/socket.io`

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `connect` | Client→Server | - | Establish connection |
| `disconnect` | Client→Server | - | Close connection |
| `chat:message` | Client→Server | `{content, sessionId, workspace}` | Send user message |
| `chat:token` | Server→Client | `string` | Streamed LLM token |
| `chat:tool_call` | Server→Client | `{id, name, arguments}` | Tool invocation started |
| `chat:tool_result` | Server→Client | `{callId, result}` | Tool execution result |
| `chat:done` | Server→Client | `{}` | Streaming complete |

---

## 💾 Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id VARCHAR PRIMARY KEY,
    session_id VARCHAR REFERENCES sessions(id),
    role VARCHAR NOT NULL,  -- 'user', 'assistant', 'tool_call'
    content TEXT,
    tool_name VARCHAR,
    tool_args TEXT,      -- JSON string
    tool_result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 Tool System

### Tool Categories
| Category | Description | Example Tools |
|----------|-------------|---------------|
| **System** | System info, processes, services | `system_info`, `process_list`, `service_manager` |
| **File Operations** | Read/write/list files | `read_file`, `write_file`, `list_directory` |
| **Network** | Port scanning, connectivity | `port_scan`, `ping`, `traceroute` |
| **Security** | Vulnerability scanning, audits | `vuln_scan`, `ssl_check`, `audit_config` |
| **Docker** | Container management | `docker_ps`, `docker_logs`, `docker_exec` |
| **Kubernetes** | K8s cluster operations | `kubectl_get`, `kubectl_logs`, `kubectl_apply` |
| **Database** | DB connections, queries | `db_query`, `db_backup` |
| **Cloud** | AWS/Azure/GCP operations | `aws_ec2_list`, `azure_vm_list` |

### Adding Custom Tools

1. Create tool class in `backend/app/tools/custom/`:
```python
from app.tools.base import BaseTool, ToolResult

class MyCustomTool(BaseTool):
    name = "my_custom_tool"
    description = "Description of what this tool does"
    category = "Custom"
    parameters = {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param1"]
    }

    async def execute(self, param1: str) -> ToolResult:
        # Implementation
        return ToolResult(output=f"Result: {param1}")
```

2. Register in `backend/app/tools/registry.py`:
```python
from app.tools.custom.my_custom_tool import MyCustomTool
tool_registry.register(MyCustomTool())
```

---

## 🎨 Frontend Structure

```
frontend/src/
├── components/
│   ├── artifacts/       # Code/artifact rendering
│   ├── chat/            # Chat interface components
│   ├── layout/          # Header, Sidebar
│   ├── monitor/         # System monitoring
│   ├── tools/           # Tool catalog
│   ├── widgets/         # Dashboard widgets
│   └── workspace/       # File explorer
├── services/
│   ├── api.ts           # REST API client
│   └── socketService.ts # WebSocket client
├── store/
│   └── useAppStore.ts   # Global Zustand store
├── types/
│   ├── index.ts         # Shared types
│   ├── chat.ts          # Message types
│   └── session.ts       # Session types
└── utils/
    └── cn.ts            # Class name utility
```

### State Management (Zustand)

```typescript
// useAppStore.ts - Key state slices
interface AppState {
  // UI State
  activeTab: 'chat' | 'tools' | 'monitor' | 'workspace' | 'widgets';
  socketStatus: 'connected' | 'connecting' | 'disconnected';
  
  // Chat State
  messages: Message[];
  sessions: Session[];
  activeSessionId: string | null;
  
  // Tools State
  tools: Tool[];
  selectedCategory: string;
  selectedTool: Tool | null;
  
  // System State
  systemMetrics: SystemMetrics | null;
  
  // Workspace State
  workspaceFiles: FileNode[];
  selectedFile: FileNode | null;
  
  // Actions
  setActiveTab: (tab) => void;
  addMessage: (msg) => void;
  updateLastAgentMessage: (token) => void;
  addToolCallToLastMessage: (toolCall) => void;
  fetchSessions: () => Promise<void>;
  setActiveSessionId: (id) => Promise<void>;
  // ... more actions
}
```

---

## 🐳 Docker Deployment

### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./AI_Agent_Web_v2.0/backend
    container_name: ai-agent-backend
    env_file:
      - ./AI_Agent_Web_v2.0/backend/.env
    ports:
      - "8000:8000"
    volumes:
      - ./AI_Agent_Web_v2.0/backend:/app
    restart: unless-stopped

  frontend:
    build: ./AI_Agent_Web_v2.0/frontend
    container_name: ai-agent-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
```

### Production Build
```bash
# Build images
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` files. Use Docker secrets or environment variables in production.
2. **CORS**: Configure `CORS_ORIGINS` to specific domains in production.
3. **Database**: SQLite is for development. Use PostgreSQL for production.
4. **WebSocket**: Consider WSS (WebSocket Secure) with reverse proxy (nginx/traefik).
5. **Authentication**: Current version has no auth. Add JWT/OAuth for production.

---

## 🧪 Testing

### Backend Tests
```bash
cd AI_Agent_Web_v2.0/backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd AI_Agent_Web_v2.0/frontend
npm run test
```

### E2E Tests
```bash
# Using Playwright
npx playwright test
```

---

## 📝 Development Guidelines

### Code Style
- **Backend**: Black formatter, Ruff linter, type hints required
- **Frontend**: ESLint + Prettier, TypeScript strict mode

### Git Workflow
```bash
# Feature branch
git checkout -b feature/new-tool

# Commit with conventional messages
git commit -m "feat: add docker container monitoring tool"

# Push and create PR
git push origin feature/new-tool
```

### Adding a New Feature
1. Backend: Add API route → Tool (if needed) → WebSocket handler
2. Frontend: Add types → API service → Store actions → Components
3. Test both locally
4. Update documentation

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| WebSocket connection failed | Check backend is running on port 8000, verify `VITE_WS_URL` |
| LLM API errors | Verify `OPENAI_API_KEY` and `OPENAI_BASE_URL` in `.env` |
| Database errors | Delete `app_data.db` and restart backend |
| Frontend build fails | Clear `node_modules`, run `npm install` again |
| Docker permission denied | Run with `sudo` or add user to docker group |

### Debug Mode
```bash
# Backend with debug logging
LOG_LEVEL=DEBUG uvicorn app.main:app --reload

# Frontend with verbose output
npm run dev -- --debug
```

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Socket.IO Docs**: https://socket.io/docs/v4
- **Zustand Docs**: https://github.com/pmndrs/zustand
- **TailwindCSS Docs**: https://tailwindcss.com/docs
- **NVIDIA Nemotron API**: https://build.nvidia.com/nvidia/nemotron-3-ultra

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Yusuf PEKER**
- GitHub: [@YusufPEKERR](https://github.com/YusufPEKERR)
- Project: [AI-AGENT](https://github.com/YusufPEKERR/AI-AGENT)

---

*Last Updated: 2026-07-23 | Version 2.0.0*