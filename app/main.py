from fastapi import FastAPI

from app.middleware.cors import setup_cors
from app.api.v1.router import api_router

# Create FastAPI app
app = FastAPI(
    title="CEIT CMS API",
    version="1.0.0",
)

# Setup CORS middleware
setup_cors(app)

# Include routers
app.include_router(api_router, prefix="/api")

# Root endpoints
@app.get("/")
async def root():
    return {"message": "API is running"}

# Migration commands:
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head