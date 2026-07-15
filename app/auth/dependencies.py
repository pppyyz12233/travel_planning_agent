"""FastAPI 依赖注入"""

from fastapi import Depends, Header, HTTPException

from app.auth.security import decode_token
from app.utils.database import AsyncSessionLocal
from app.crud.user import get_by_id


async def get_current_user(authorization: str = Header(...)):
    """从 Authorization: Bearer <token> 解析当前用户"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="缺少 Bearer Token")

    try:
        payload = decode_token(authorization[7:])
    except Exception:
        raise HTTPException(status_code=401, detail="Token 无效或已过期")

    async with AsyncSessionLocal() as db:
        return await get_by_id(db, int(payload["sub"]))


async def require_admin(user=Depends(get_current_user)):
    """要求管理员角色"""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user
