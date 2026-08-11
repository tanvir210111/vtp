# 🛠️ Setup & Deployment Guide

## Prerequisites

- **Node.js**: v18.0.0 or higher
- **Python**: v3.11 or higher
- **FFmpeg**: (Optional for local execution, bundled in Docker)

---

## Environment Configuration

Copy `.env.example` or create `.env` in `backend/` and `frontend/`:

### `backend/.env`
```env
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000
DATABASE_URL=sqlite:///./database/sqlite.db
STORAGE_PATH=../storage
OUTPUT_PATH=../output
DEFAULT_MAX_FILE_SIZE_MB=200
```

### `frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## Production Deployment with Docker Compose

```bash
cd docker
docker-compose up --build -d
```

Check system status:
```bash
docker-compose logs -f
```
