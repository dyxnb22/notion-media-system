import requests

from app.config import settings


class NotionService:
    """
    Notion 写入服务

    负责：
    - 调用 Notion API
    - 创建媒体记录页面
    """

    BASE_URL = "https://api.notion.com/v1/pages"

    def create_media_page(self, media_data: dict):
        """
        创建 Notion 页面。

        media_data:
        {
            title,
            media_type,
            cover,
            source,
            source_id
        }
        """

        headers = {
            "Authorization": f"Bearer {settings.NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

        payload = {
            "parent": {
                "database_id": settings.NOTION_DATABASE_ID
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": media_data["title"]
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": media_data["media_type"]
                    }
                },
                "Source": {
                    "select": {
                        "name": media_data["source"]
                    }
                }
            }
        }

        # 如果有封面，则设置页面封面
        if media_data.get("cover"):
            payload["cover"] = {
                "type": "external",
                "external": {
                    "url": media_data["cover"]
                }
            }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


notion_service = NotionService()
