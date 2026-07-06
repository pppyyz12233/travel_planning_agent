"""认证相关 Pydantic Schema"""

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64, examples=["traveler01"])
    password: str = Field(min_length=6, max_length=128, examples=["mySecurePass123"])


class LoginRequest(BaseModel):
    username: str = Field(examples=["traveler01"])
    password: str = Field(examples=["mySecurePass123"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: str
