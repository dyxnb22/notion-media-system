from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.search import router as search_router
from app.routers.media import router as media_router

# FastAPI 应用入口
# 所有 API 都会从这里启动

app = FastAPI(
    title="Notion Media System",
    description="个人媒体记录系统后端",
    version="0.1.0"
)

# 允许前端跨域访问
# 开发阶段直接允许全部
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(search_router)
app.include_router(media_router)


@app.get("/health")
def health_check():
    """
    健康检查接口

    用于：
    - Docker 健康检查
    - 判断后端是否启动成功
    - Nginx / Cloudflare 探活
    """

    return {
        "status": "ok"
    }
