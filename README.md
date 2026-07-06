<div align="center">

<h1>
  ✈️ Smart Travel Planner
  <br/>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=flat-square" /></a>
  <a href="#"><img src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white&style=flat-square" /></a>
  <a href="#"><img src="https://img.shields.io/badge/LangGraph-0.2+-7B3FE4?style=flat-square" /></a>
  <a href="#"><img src="https://img.shields.io/badge/LLM-DeepSeek-536DFE?style=flat-square" /></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" /></a>
</h1>

<h3>💬 一句话，搞定整个旅程</h3>

<sub>Plan-and-Execute × ReAct · 多 Agent 协作 · MCP 工具协议 · RAG 混合检索 · DeepEval 测试</sub>

</div>

---

## 💡 这是什么

"下个月从上海去东京，5 天，预算 1 万" → AI 自动规划航班、酒店、景点、日程、预算。

```
用户输入
  │
  ▼
┌─────────┐
│  Guard  │  正则拦截攻击/越狱/交易 → 拒绝（零 Token）
└────┬────┘
     │ 通过
     ▼
┌──────────────────────────────┐
│        Supervisor            │
│                              │
│  Plan ──→ ① ✈️航班  ② 🏨酒店  │
│           ③ 🎯景点  ④ 📅日程  │
│           ⑤ 💰预算           │
│     │                        │
│  Execute ──→ 逐步调度 Worker  │
│     │                        │
│  每个 Worker = ReAct 循环     │
│  🤔 思考 → 🔧 行动 → 👁️ 观察  │
│  调 MCP 工具 / RAG 知识库     │
└──────────────┬───────────────┘
               │
               ▼
     📋 完整旅行方案 + 预算明细
```

---

## 🚀 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env        # 填 DEEPSEEK_API_KEY
python main.py              # → http://localhost:8000/docs
```

---

## 🏗 架构

| 层级 | 模式 | 说明 |
|:--|:--|:--|
| 主 Agent（Supervisor） | Plan-and-Execute | 分析意图 → 生成计划 → 逐步调度 Worker |
| Worker（×5） | ReAct | Thought → Action → Observation 循环 |

### 五个 Worker

| Worker | 职责 | 工具 |
|:--|:--|:--|
| ✈️ `flight` | 航班搜索 | MCP 航班 Server |
| 🏨 `hotel` | 酒店推荐 | MCP + RAG |
| 🎯 `attraction` | 景点攻略 | RAG |
| 📅 `itinerary` | 日程编排 | 综合前序结果 |
| 💰 `budget` | 预算汇总 | 综合前序结果 |

---

## 🛡 安全

- **Guard**：正则匹配违规输入 → 直接拒绝，不消耗 LLM Token
- **SKILL.md**：每个 Worker 加载角色说明书，严格限定能力边界
- **零真实交易**：所有输出为建议文本，不执行购买 / 支付 / 下单

---

## 📦 项目结构

```
travel_planning_agent/
├── main.py                              # 启动入口
├── .env.example                         # 环境变量模板
├── .gitignore
├── requirements.txt                     # Python 依赖
├── README.md
│
├── app/
│   ├── utils/                           # 基础设施
│   │   ├── config.py                    # Pydantic Settings 读取 .env
│   │   ├── database.py                  # SQLite 异步引擎 + 会话工厂
│   │   ├── exceptions.py               # 全局异常类
│   │   ├── llm.py                       # DeepSeek AsyncOpenAI 封装
│   │   └── context_manager.py          # Token 预算 + 滑动窗口 + 语义压缩
│   │
│   ├── models/                          # SQLAlchemy ORM（5 张表）
│   │   ├── __init__.py                  # 聚合导出 Base + 5 个模型
│   │   ├── base.py                      # declarative_base
│   │   ├── user.py                      # User ─ id/username/password_hash/salt/role
│   │   ├── message.py                   # Message ─ 对话消息
│   │   ├── plan.py                      # Plan ─ 旅行计划
│   │   ├── document.py                 # Document ─ 上传文档元数据
│   │   └── conversation.py             # Conversation ─ 对话会话
│   │
│   ├── crud/                            # 数据访问层
│   │   ├── base.py                      # 泛型 CRUD 基类
│   │   ├── user.py                      # User 增删改查
│   │   ├── message.py                   # Message 增删改查
│   │   ├── plan.py                      # Plan 增删改查
│   │   ├── document.py                 # Document 增删改查
│   │   └── conversation.py             # Conversation 增删改查
│   │
│   ├── schemas/                         # Pydantic 请求/响应模型
│   │   ├── auth.py                      # 注册/登录/Token
│   │   ├── chat.py                      # 对话/历史
│   │   ├── knowledge.py                # 知识库检索
│   │   └── admin.py                     # 管理接口
│   │
│   ├── auth/                            # 认证鉴权
│   │   ├── security.py                  # SHA-256 加盐 + JWT 签发验证
│   │   └── dependencies.py             # get_current_user / require_admin
│   │
│   ├── routers/                         # FastAPI 路由
│   │   ├── router.py                    # APIRouter 聚合
│   │   ├── auth_router.py              # POST /register /login + GET /me
│   │   ├── chat_router.py              # POST /chat（SSE） + GET /history
│   │   ├── admin_router.py             # 用户管理 + POST /upload（文档入库）
│   │   └── knowledge_router.py         # GET /search-knowledge（RAG 调试）
│   │
│   ├── agents/                          # Agent 核心
│   │   ├── state.py                     # AgentState TypedDict
│   │   ├── supervisor.py               # LangGraph Plan-and-Execute 主图
│   │   ├── skills/                      # 各 Worker 的角色说明书（Markdown）
│   │   │   ├── planner.md              # Planner 计划拆解规范
│   │   │   ├── flight.md               # 航班 Worker
│   │   │   ├── hotel.md                # 酒店 Worker
│   │   │   ├── attraction.md           # 景点 Worker
│   │   │   ├── itinerary.md            # 日程 Worker
│   │   │   └── budget.md               # 预算 Worker
│   │   ├── workers/                     # Worker 实现
│   │   │   ├── base.py                  # Worker 基类（RSKILL.md + ReAct 循环）
│   │   │   ├── flight_worker.py        # 航班 Worker
│   │   │   ├── hotel_worker.py         # 酒店 Worker
│   │   │   ├── attraction_worker.py    # 景点 Worker
│   │   │   ├── itinerary_worker.py     # 日程 Worker
│   │   │   └── budget_worker.py        # 预算 Worker
│   │   └── workflow/                    # 确定性规则层
│   │       └── guard.py                 # 输入安全校验（正则，零 Token）
│   │
│   ├── mcp/                             # MCP 协议层
│   │   ├── client.py                    # MCP Client ─ Agent 调工具入口
│   │   ├── registry.py                 # 工具注册表（启动时加载）
│   │   └── servers/
│   │       ├── flight_server.py        # 航班 MCP Server（模拟数据）
│   │       └── weather_server.py       # 天气 MCP Server（模拟数据）
│   │
│   └── rag/                             # RAG 知识检索管道
│       ├── mineru_parser.py            # PDF/Word → Markdown
│       ├── chunker.py                  # Markdown → 语义分块（512/128）
│       ├── embeddings.py              # BGE-M3 向量化
│       ├── bm25.py                     # BM25 关键词检索
│       ├── retriever.py               # 混合检索 + CrossEncoder 精排 → Top5
│       └── vector_store.py            # ChromaDB CRUD
│
├── uploads/                             # 管理员上传文件落盘
│   └── .gitkeep
│
└── tests/                               # DeepEval 测试
    ├── conftest.py                      # Fixtures
    ├── test_supervisor.py             # Supervisor 测试 ×3
    ├── test_flight_worker.py          # 航班 Worker 测试 ×3
    ├── test_hotel_worker.py           # 酒店 Worker 测试 ×3
    ├── test_attraction_worker.py      # 景点 Worker 测试 ×3
    ├── test_itinerary_worker.py       # 日程 Worker 测试 ×3
    └── test_budget_worker.py          # 预算 Worker 测试 ×3
```## 🧪 技术栈

| 分类 | 技术 |
|:--|:--|
| Agent | LangGraph · ReAct · Plan-and-Execute |
| LLM | DeepSeek (AsyncOpenAI) |
| 工具 | MCP 协议（航班 + 天气模拟 Server） |
| 检索 | BGE-M3 · BM25 · CrossEncoder · ChromaDB |
| 文档 | MinerU（PDF/Word → Markdown） |
| Web | FastAPI · uvicorn · SSE 流式 |
| 数据 | SQLite · SQLAlchemy async |
| 认证 | SHA-256 加盐 · JWT HS256 |
| 上下文 | tiktoken 滑动窗口 · 语义压缩 |
| 测试 | DeepEval（AnswerCorrectness + ToolCallAccuracy） |

---

## 📄 License

MIT

