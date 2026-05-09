import requests

from app.config import settings
from app.schemas import MediaSearchResult


class RawgGameProvider:
    """
    RAWG 游戏搜索提供者

    负责：
    - 调用 RAWG API
    - 搜索游戏
    - 转换成统一数据结构
    """

    BASE_URL = "https://api.rawg.io/api/games"

    def search(self, query: str):
        """
        根据关键词搜索游戏。

        参数：
        - query: 用户输入的游戏名称，比如 "Resident Evil 4"

        返回：
        - List[MediaSearchResult]
        """

        if not settings.RAWG_API_KEY:
            # 没配置 API Key 时，直接返回空列表，避免程序崩溃
            return []

        params = {
            "key": settings.RAWG_API_KEY,
            "search": query,
            "page_size": 10,
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for game in data.get("results", []):
            results.append(
                MediaSearchResult(
                    source_id=str(game["id"]),
                    title=game["name"],
                    original_title=game["name"],
                    year=game.get("released"),
                    cover=game.get("background_image"),
                    media_type="game",
                    source="RAWG",
                )
            )

        return results
