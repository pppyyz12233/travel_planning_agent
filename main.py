from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
"""启动入口"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.utils.database import init_db
from app.mcp.registry import init_registry
from app.routers import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：建表 + 注册工具
    await init_db()
    init_registry()
    yield


app = FastAPI(
    title="智能旅行规划师",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), name='static')
@app.get('/')
async def root():
    return FileResponse('index.html')


app.include_router(api_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
