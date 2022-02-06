from fastapi import APIRouter
from app.api.endpoints import doc
from app.api.endpoints import healthcheck

api_router = APIRouter()
api_router.include_router(doc.router, tags=["doc"])
api_router.include_router(healthcheck.router, tags=["healthcheck"])
