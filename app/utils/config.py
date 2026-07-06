"""全局配置 —— 读取 .env 环境变量"""

import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))

# SQLite
SQLITE_PATH = os.getenv("SQLITE_PATH", "sqlite+aiosqlite:///./travel.db")

# ChromaDB
CHROMA_PERSIST_PATH = os.getenv("CHROMA_PERSIST_PATH", "./chroma_data")

# MinerU
MINERU_ENABLED = os.getenv("MINERU_ENABLED", "false").lower() == "true"

# Agent
MAX_TOOL_ITERATIONS = int(os.getenv("MAX_TOOL_ITERATIONS", "3"))
