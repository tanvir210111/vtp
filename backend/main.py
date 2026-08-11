"""
FastAPI Server Entry Point matching exact REST API specification.
"""
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from database.database import Base, engine
from api import health, upload, generate, history, download

# Create DB tables
Base.metadata.create_all(bind=engine)

# Ensure storage directories exist
os.makedirs(os.path.join(settings.STORAGE_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_DIR, "frames"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_DIR, "thumbnails"), exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    description="Video to AI Prompt generator REST backend API server.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Custom Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": str(exc)}
    )

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Directories for thumbnails and media access
app.mount("/storage", StaticFiles(directory=settings.STORAGE_DIR), name="storage")

# Register API Routers under /api prefix
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(upload.router, prefix=settings.API_V1_STR)
app.include_router(generate.router, prefix=settings.API_V1_STR)
app.include_router(history.router, prefix=settings.API_V1_STR)
app.include_router(download.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
