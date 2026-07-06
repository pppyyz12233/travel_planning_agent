"""SHA-256 加盐哈希 + JWT 签发/验证"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.utils.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_HOURS


def hash_password(password: str) -> "tuple[str, str]":
    """返回 (hash_hex, salt_hex)"""
    salt = secrets.token_hex(16)
    salted = salt + password
    hash_hex = hashlib.sha256(salted.encode()).hexdigest()
    return hash_hex, salt


def verify_password(password: str, salt: str, hash_value: str) -> bool:
    """验证密码"""
    return hashlib.sha256((salt + password).encode()).hexdigest() == hash_value


def create_token(user_id: int, role: str) -> str:
    """签发 JWT"""
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """验证并解码 JWT，无效则抛出异常"""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
