from fastapi import APIRouter

from src.presentation.auth.routes import AuthRoutes
from src.presentation.chat.routes import ChatRoutes


class AppRoutes:
    
    @staticmethod
    def get_routes() -> APIRouter:
        router = APIRouter()
        router.include_router(AuthRoutes.get_routes())
        router.include_router(ChatRoutes.get_routes())
        return router


