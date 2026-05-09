# Notion Media System

一个用 **FastAPI + Next.js + Notion API** 做的个人媒体记录系统。

第一版目标：

```text
前端输入媒体名称和类别
↓
后端调用第三方 API 搜索候选结果
↓
返回多个封面和基础信息
↓
用户选择一个结果
↓
后端写入 Notion Database
```

当前初版先重点支持：

- 游戏搜索：RAWG API
- 统一媒体模型：后续可以扩展电影、电视剧、动漫
- Notion 写入：保存标题、类别、封面、年份、来源等字段

---

## 项目结构

```text
notion-media-system/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── config.py         # 环境变量配置
│   │   ├── schemas.py        # 请求/响应数据结构
│   │   ├── routers/          # API 路由层
│   │   ├── providers/        # 第三方媒体数据源
│   │   └── services/         # 业务逻辑层
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Next.js 前端
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx          # 搜索和选择封面的页面
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml        # 本地/服务器一键启动
├── .env.example              # 环境变量示例
└── .gitignore
```

---

## 模块说明

### 1. frontend 前端模块

负责用户交互：

1. 用户选择类别，比如 `game`
2. 输入名称，比如 `生化危机4`
3. 点击搜索
4. 前端请求后端 `/api/search`
5. 展示多个候选结果
6. 用户点击某个候选结果
7. 前端请求后端 `/api/media`
8. 后端保存到 Notion

第一版页面在：

```text
frontend/app/page.tsx
```

---

### 2. backend 路由层

路由层只负责接收请求和返回响应，不写复杂业务。

```text
backend/app/routers/search.py
backend/app/routers/media.py
```

接口：

```text
GET  /api/search?type=game&q=resident evil 4
POST /api/media
GET  /health
```

---

### 3. providers 数据源模块

第三方 API 统一放这里。

```text
backend/app/providers/base.py
backend/app/providers/rawg.py
```

现在只有 RAWG 游戏搜索。

后面扩展电影/电视剧/动漫时，不需要重构系统，只要新增：

```text
TmdbProvider
AniListProvider
```

然后在 `media_service.py` 里注册即可。

---

### 4. services 业务层

业务层负责把路由和具体数据源连接起来。

```text
backend/app/services/media_service.py
backend/app/services/notion_service.py
```

业务走向：

```text
search.py
↓
media_service.search_media()
↓
RawgGameProvider.search()
↓
返回统一格式 MediaSearchResult
```

保存走向：

```text
media.py
↓
notion_service.create_media_page()
↓
Notion API
↓
你的 Notion Database
```

---

## Notion Database 字段建议

你的 Notion Database 建议创建这些字段：

| 字段名 | 类型 | 说明 |
|---|---|---|
| Name | Title | 媒体名称 |
| Type | Select | game / movie / tv / anime |
| Original Name | Rich text | 原始名称 |
| Year | Number | 年份 |
| Cover | URL | 封面链接 |
| Source | Select | RAWG / TMDB / AniList |
| Source ID | Rich text | 第三方平台 ID |
| Status | Select | planned / playing / completed |
| Notes | Rich text | 备注 |

注意：Notion 的字段名要和代码里保持一致。

---

## 环境变量

复制：

```bash
cp .env.example .env
```

填写：

```env
RAWG_API_KEY=你的_RAWG_KEY
NOTION_TOKEN=你的_NOTION_INTEGRATION_TOKEN
NOTION_DATABASE_ID=你的_NOTION_DATABASE_ID
```

---

## 本地启动后端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：

```text
http://localhost:8000/docs
```

---

## 本地启动前端

```bash
cd frontend
npm install
npm run dev
```

访问：

```text
http://localhost:3000
```

---

## Docker 启动

```bash
docker compose up -d --build
```

访问：

```text
前端：http://服务器IP:3000
后端：http://服务器IP:8000/docs
```

---

## 后续扩展方向

推荐顺序：

1. 先把游戏搜索跑通
2. 接 Notion 保存
3. 加电影/电视剧：TMDB API
4. 加动漫：AniList API
5. 加登录
6. 加 PostgreSQL 做缓存
7. 加 AI 推荐和年度总结
