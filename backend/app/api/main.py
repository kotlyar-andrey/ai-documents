from fastapi import APIRouter

from .routes import chat, documents

api_router = APIRouter()

api_router.include_router(chat.router)
api_router.include_router(documents.router)
api_router.include_router(documents.router)
api_router.include_router(documents.router)
