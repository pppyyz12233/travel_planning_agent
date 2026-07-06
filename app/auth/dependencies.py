"""FastAPI 依赖注入：认证 + 鉴权"""

from fastapi import Depends, Header

from app.auth.security import decode_token
from app.crud.user import UserCRUD
from app.models.user import User
from app.utils.database import async_session
from app.utils.exceptions import ForbiddenError, UnauthorizedError


async def get_current_user(authorization: str = Header(...)) -> User:
    """从 Authorization: Bearer <token> 解析当前用户"""
    if not authorization.startswith("Bearer "):
        raise UnauthorizedError("缺少 Bearer Token")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_token(token)
    except Exception:
        raise UnauthorizedError("Token 无效或已过期")

    user_id = int(payload["sub"])
    async with async_session() as db:
        repo = UserCRUD(db)
        user = await repo.get_by_id(user_id)
        if user is None:
            raise UnauthorizedError("用户不存在")
        return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    """要求管理员角色"""
    if user.role != "admin":
        raise ForbiddenError("需要管理员权限")
    return user
