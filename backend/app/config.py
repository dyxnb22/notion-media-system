from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    项目环境变量配置

    所有敏感配置统一放这里：
    - API Key
    - Token
    - 数据库配置
    """

    RAWG_API_KEY: str = ""

    NOTION_TOKEN: str = ""
    NOTION_DATABASE_ID: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
