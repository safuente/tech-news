from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from core.logger import logger
from core.redis import redis_manager

# ===== Lifespan Events =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    # Startup
    logger.info("🚀 Starting News Dashboard API...")
    
    # Connect to Redis
    await redis_manager.connect()
    logger.info("✅ Redis connected")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")
    await redis_manager.disconnect()
    logger.info("✅ Redis disconnected")

# ===== FastAPI Application =====
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="News Dashboard API with Redis caching",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ===== CORS Middleware =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"✅ CORS enabled for: {settings.get_cors_origins}")

# ===== Health Check Endpoints =====
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/ping", tags=["Health"])
async def ping():
    """Simple health check endpoint"""
    logger.info("Ping endpoint called")
    return {
        "status": "ok",
        "message": "pong"
    }

@app.get("/health", tags=["Health"])
async def health():
    """Detailed health check with Redis status"""
    redis_status = "connected" if redis_manager.redis else "disconnected"
    
    health_info = {
        "status": "healthy" if redis_status == "connected" else "degraded",
        "api": "running",
        "redis": redis_status,
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }
    
    logger.info(f"Health check: {health_info}")
    return health_info

# ===== Include Routers =====
# TODO: Uncomment when news router is ready
from routers import news
app.include_router(news.router, prefix="/api/news", tags=["News"])

logger.info("✅ API routers registered")