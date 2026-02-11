"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import ask_ai, marimo, notebooks, videos
from .monitoring import configure_logfire

# Configure monitoring before app initialization
configure_logfire()

app = FastAPI(
    title="Manimo API",
    description="AI-native notebook orchestrator for Manim animations",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ask_ai.router, prefix="/api", tags=["ai"])
app.include_router(marimo.router, prefix="/api", tags=["marimo"])
app.include_router(notebooks.router, prefix="/api", tags=["notebooks"])
app.include_router(videos.router, prefix="/api", tags=["videos"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Manimo API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

