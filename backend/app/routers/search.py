from fastapi import APIRouter, Query

from app.services.media_service import media_service

router = APIRouter(prefix="/api", tags=["Search"])


@router.get("/search")
def search_media(
    type: str = Query(..., description="媒体类型，比如 game"),
    q: str = Query(..., description="搜索关键词")
):
    """
    统一媒体搜索接口。

    示例：

    /api/search?type=game&q=resident evil 4

    业务流程：

    前端
    ↓
    search.py
    ↓
    media_service
    ↓
    provider
    ↓
    第三方 API
    ↓
    返回统一数据结构
    """

    return media_service.search_media(type, q)
