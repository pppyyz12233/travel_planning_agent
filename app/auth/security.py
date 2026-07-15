
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.utils.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_HOURS


def hash_password(password: str) -> str:
    """返回 salt$hash 格式"""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain: str, hashed: str) -> bool:
    """验证密码"""
    parts = hashed.split("$")
    if len(parts) != 2:
        return False
    salt, stored = parts
    return hashlib.sha256((plain + salt).encode()).hexdigest() == stored


def create_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
