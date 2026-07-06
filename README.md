<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-0.2+-purple" alt="LangGraph">
  <img src="https://img.shields.io/badge/DeepSeek-API-536DFE" alt="DeepSeek">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

<h1 align="center">✈️ Smart Travel Planner</h1>
<p align="center"><b>Plan-and-Execute × ReAct · 只说一句话，AI 搞定整个旅程</b></p>

---

## 怎么工作的

```
"下个月从上海去东京，5 天，人均预算 1 万"

        │
        ▼
  ┌─────────────┐
  │   Guard     │  安全门禁：正则拦截违规输入，不过关直接驳回
  └──────┬──────┘
         │
         ▼
  ┌─────────────────────────────────────┐
  │         Supervisor                  │
  │                                     │
  │  Plan ───→ 生成执行计划:             │
  │           ① 查航班                   │
  │           ② 查酒店                   │
  │           ③ 推荐景点                 │
  │           ④ 编排日程                 │
  │           ⑤ 计算预算                 │
  │     │                               │
  │     ▼                               │
  │  Execute ─→ 逐步调度 Worker          │
  │                                     │
  │  ┌──────┬──────┬──────────┬───────┬──────┐
  │  │✈️航班│🏨酒店│ 🎯景点   │📅日程│💰预算│
  │  └──┬───┴──┬───┴────┬─────┴──┬────┴──┬───┘
  │     │      │        │        │       │
  │     │   每个 Worker = ReAct 循环      │
  │     │   🤔 思考 → 🔧 行动 → 👁️ 观察   │
  │     │   调用 MCP 工具 / RAG 知识库    │
  └─────┼──────┼────────┼────────┼───────┘
        └──────┴────────┴────────┘
                    │
                    ▼
         📋 完整旅行方案
         · 航班推荐  · 酒店列表  · 景点攻略
         · 每日日程  · 预算明细
```

---

## 亮点

| ✨ | |
|:--|:--|
| **Plan-and-Execute** | 复杂任务自动拆解成多步计划，逐步推进，出错可重试 |
| **ReAct Worker** | 每个 Worker 内是完整的 Thought→Action→Observation 循环，透明可解释 |
| **安全前置** | Guard 固定规则过滤违规输入，不靠 LLM 判断，零 Token 消耗 |
| **MCP 协议** | 工具与 Agent 解耦，加新工具不改 Agent 代码 |
| **RAG 混合检索** | BGE-M3 向量 + BM25 关键词 + CrossEncoder 精排，三管齐下 |
| **MinerU** | PDF/Word 上传自动解析入库，知识越养越丰富 |

---

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env          # 填 DEEPSEEK_API_KEY
python main.py                # → http://localhost:8000/docs
```

---

## 项目骨架

```
travel_planning_agent/
│
├── main.py                         启动入口
├── .env.example                    环境变量模板
├── requirements.txt
│
└── app/
    ├── utils/         config / db / llm / context / exceptions
    ├── models/        5 张表 ─ User · Message · Plan · Document · Conversation
    ├── crud/          数据访问层，每表一个
    ├── schemas/       Pydantic 请求/响应
    ├── auth/          SHA-256 + JWT
    ├── routers/       chat · auth · admin · knowledge
    │
    ├── agents/        ★ 核心
    │   ├── supervisor.py    Plan-and-Execute 主图
    │   ├── state.py         状态定义
    │   ├── skills/          每个 Worker 的角色说明书 (.md)
    │   ├── workers/         ReAct Worker × 5
    │   └── workflow/        guard 安全门禁
    │
    ├── mcp/           航班 Server · 天气 Server · Client · Registry
    ├── rag/           MinerU · Chunker · BGE-M3 · BM25 · Retriever · ChromaDB
    │
    ├── uploads/       管理员上传的 PDF/Word 落盘
    └── tests/         DeepEval ─ AnswerCorrectness + ToolCallAccuracy
```

---

## 技术栈

```
FastAPI  ·  LangGraph  ·  DeepSeek  ·  MCP  ·  ReAct
BGE-M3  ·  BM25  ·  CrossEncoder  ·  ChromaDB  ·  MinerU
SQLite  ·  SQLAlchemy  ·  JWT  ·  DeepEval
```

---

## License

MIT —— 随便用，玩得开心 ✈️
