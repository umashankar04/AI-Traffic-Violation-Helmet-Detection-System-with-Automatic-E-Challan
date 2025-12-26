"""
FastAPI Application Main Entry Point
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import logging
import os
import secrets

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify username and password"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Initialize FastAPI app
app = FastAPI(
    title="Traffic Violation Detection API",
    description="AI-powered Traffic Violation & Helmet Detection System with Automatic E-Challan",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZIP compression handled by reverse proxy in production


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Health check endpoint (no auth needed)
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Traffic Violation Detection API",
        "version": "1.0.0"
    }


@app.get("/")
async def root(user: str = Depends(verify_credentials)):
    """Root endpoint - requires authentication."""
    return {
        "message": f"Welcome {user} to Traffic Violation Detection API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "webcam_interface": "/webcam",
        "endpoints": {
            "violations": "/api/violations",
            "challan": "/api/challan",
            "analytics": "/api/analytics",
            "camera": "/api/camera"
        }
    }


@app.get("/webcam")
async def webcam_interface(user: str = Depends(verify_credentials)):
    """Serve real-time webcam interface - requires authentication"""
    html_path = os.path.join(
        os.path.dirname(__file__),
        "../../frontend/html/index.html"
    )
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    return {
        "error": "Webcam interface not found",
        "available_endpoints": [
            "/api/camera/start",
            "/api/camera/stop",
            "/api/camera/stream",
            "/api/camera/capture",
            "/api/camera/detect-violation"
        ]
    }


# Register routers
from backend.app.routes.violations import router as violations_router
from backend.app.routes.challan import router as challan_router
from backend.app.routes.analytics import router as analytics_router
from backend.app.routes.camera import router as camera_router

app.include_router(violations_router)
app.include_router(challan_router)
app.include_router(analytics_router)
app.include_router(camera_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup."""
    logger.info("Starting Traffic Violation Detection API")
    
    # Initialize database
    try:
        from backend.app.database.database import init_db
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database not available: {str(e)}")
        logger.warning("Running in limited mode without database persistence")
        logger.warning("To enable full features, start a PostgreSQL database on localhost:5432")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Traffic Violation Detection API")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        workers=1
    )
