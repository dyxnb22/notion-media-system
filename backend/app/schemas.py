from pydantic import BaseModel
from typing import Optional


class MediaSearchResult(BaseModel):
    """
    统一媒体搜索结果结构

    不管是：
    - 游戏
    - 电影
    - 动漫

    最后都统一转换成这个格式。
    """

    source_id: str
    title: str
    original_title: Optional[str] = None
    year: Optional[str] = None
    cover: Optional[str] = None
    media_type: str
    source: str


class CreateMediaRequest(BaseModel):
    """
    保存到 Notion 的请求结构
    """

    title: str
    media_type: str
    original_title: Optional[str] = None
    year: Optional[str] = None
    cover: Optional[str] = None
    source: str
    source_id: str
