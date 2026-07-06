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
app/
├── utils/         基础设施（config · db · llm · context）
├── models/        5 张表 ─ User · Message · Plan · Document · Conversation
├── crud/          数据访问层（每表一个）
├── schemas/       Pydantic 请求/响应模型
├── auth/          SHA-256 加盐 + JWT
├── routers/       FastAPI 路由（auth · chat · admin · knowledge）
├── agents/        ★ Supervisor + 5 Worker + Guard + 6 SKILL.md
├── mcp/           MCP 航班 Server + 天气 Server + Registry
└── rag/           MinerU → Chunk → BGE-M3 → BM25 → CrossEncoder → ChromaDB
```

---

## 🧪 技术栈

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

