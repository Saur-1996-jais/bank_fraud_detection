from fastapi import APIRouter
from backend.app.api.routes.auth import register, activate
from .routes import home

api_router = APIRouter()

api_router.include_router(home.router)
api_router.include_router(register.router)
api_router.include_router(activate.router)