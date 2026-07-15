"""全局配置"""

import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

JWT_SECRET = os.getenv("JWT_SECRET", "a-very-long-dev-secret-key-32chars!-safe")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))

# MySQL
DB_URL = os.getenv(
    "DB_URL",
    "mysql+aiomysql://root:123456@localhost:3306/travel_planning_agent?charset=utf8mb4",
)

CHROMA_PERSIST_PATH = os.getenv("CHROMA_PERSIST_PATH", "./chroma_data")
MINERU_ENABLED = os.getenv("MINERU_ENABLED", "false").lower() == "true"
MAX_TOOL_ITERATIONS = int(os.getenv("MAX_TOOL_ITERATIONS", "3"))
