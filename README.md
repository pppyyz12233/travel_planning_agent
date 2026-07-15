<div align="center">

# ✈️ Smart Travel Planner

### Plan-and-Execute × ReAct Multi-Agent 旅行规划系统

*一句话搞定航班、酒店、景点、日程、预算*




<img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python"/>
<img src="https://img.shields.io/badge/LangGraph-0.2+-7B3FE4?style=flat-square" alt="LangGraph"/>
<img src="https://img.shields.io/badge/LLM-DeepSeek-536DFE?style=flat-square" alt="DeepSeek"/>
<img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"/>

<br/><br/>
</div>
---

## 架构

```
Supervisor (主 Agent, Plan-and-Execute)
  ├── Planner: 拆解用户需求 → JSON 计划
  └── Executor: 逐步调度 5 个 Worker
        │
        ├── ✈️ Flight    ── ReAct → MCP flight_server
        ├── 🏨 Hotel     ── ReAct → MCP hotel_server
        ├── 🎯 Attraction── ReAct → 纯 LLM 推理
        ├── 📅 Itinerary ── ReAct → MCP weather_server
        └── 💰 Budget    ── ReAct → MCP exchange_server

Guard (正则拦截) → Clarifier (追问) → Planner → Executor → Aggregator
```

| 层级 | 模式 | 说明 |
|------|------|------|
| 主 Agent | Plan-and-Execute | 分析意图 → 生成计划 → 逐步调度 → 汇总 |
| Worker ×5 | ReAct | Thought → Action → Observation 循环 |

---

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env        # 填 DEEPSEEK_API_KEY
python main.py              # → http://localhost:8000
```

---

## 项目结构

```
travel_planning_agent/
├── main.py                        启动入口
├── app/
│   ├── utils/          config / db / llm / context_manager
│   ├── models/         User · Message · Plan · Document · Conversation
│   ├── crud/           数据访问层
│   ├── schemas/        Pydantic 请求/响应
│   ├── auth/           SHA-256 加盐 + JWT
│   ├── routers/        chat · auth · admin
│   ├── agents/         ★ Supervisor + 5 Worker + Guard + SKILL.md
│   ├── mcp/            flight · hotel · weather · exchange Server
│   └── static/         Leaflet / Marked 前端依赖
├── index.html          前端（列列：表单 | 对话 | 地图）
├── .env.example
└── requirements.txt
```

---

## Worker 与工具对应

| Worker | 工具来源 | 具体工具 | 数据 |
|--------|---------|---------|------|
| ✈️ flight | MCP flight_server | search_flights / get_flight_price | 模拟 8 条 |
| 🏨 hotel | MCP hotel_server | search_hotels | 模拟 15 家 |
| 🎯 attraction | — | 纯 LLM 推理 | — |
| 📅 itinerary | MCP weather_server | get_weather / get_forecast | wttr.in |
| 💰 budget | MCP exchange_server | get_exchange_rate | exchangerate-api |

---

## 技术栈

```
LangGraph · DeepSeek · MCP · ReAct · Plan-and-Execute
FastAPI · MySQL · JWT · Leaflet · Markdown 渲染
```

---

## License

MIT