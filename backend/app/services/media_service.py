from app.providers.rawg import RawgGameProvider


class MediaService:
    """
    统一媒体服务层

    这个类的作用：
    - 根据媒体类型选择不同 Provider
    - 统一返回结果

    未来扩展：
    - movie -> TMDB
    - tv -> TMDB
    - anime -> AniList
    """

    def __init__(self):

        # 注册所有媒体 Provider
        self.providers = {
            "game": RawgGameProvider(),
        }

    def search_media(self, media_type: str, query: str):
        """
        搜索媒体。

        参数：
        - media_type: game / movie / anime
        - query: 用户输入内容
        """

        provider = self.providers.get(media_type)

        if not provider:
            raise ValueError(f"Unsupported media type: {media_type}")

        return provider.search(query)


# 单例对象
media_service = MediaService()
