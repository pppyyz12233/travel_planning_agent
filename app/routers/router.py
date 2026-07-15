"""路由聚合"""
from fastapi import APIRouter
from app.routers import auth_router, chat_router, admin_router

router = APIRouter(prefix="/api")
router.include_router(auth_router.router)
router.include_router(chat_router.router)
router.include_router(admin_router.router)