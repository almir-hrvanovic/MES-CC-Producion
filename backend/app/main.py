"""
MES Production Scheduling System - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.connection import engine
from app.database.models import Base
from app.api import work_orders, scheduling, machines


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting MES Production Scheduling System...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    print("🛑 Shutting down MES Production Scheduling System...")


# Create FastAPI application
app = FastAPI(
    title="MES Production Scheduling System",
    description="Enterprise Manufacturing Execution System for production planning and scheduling",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(work_orders.router, prefix="/api/work-orders", tags=["work-orders"])
app.include_router(scheduling.router, prefix="/api/schedule", tags=["scheduling"])
app.include_router(machines.router, prefix="/api/machines", tags=["machines"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MES Production Scheduling System API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mes-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)