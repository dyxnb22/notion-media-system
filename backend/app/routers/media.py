from fastapi import APIRouter

from app.schemas import CreateMediaRequest
from app.services.notion_service import notion_service

router = APIRouter(prefix="/api", tags=["Media"])


@router.post("/media")
def create_media(data: CreateMediaRequest):
    """
    保存媒体到 Notion。

    前端业务流程：

    用户选择封面
    ↓
    POST /api/media
    ↓
    notion_service
    ↓
    Notion Database
    """

    result = notion_service.create_media_page(data.model_dump())

    return {
        "success": True,
        "notion_page_id": result["id"]
    }
