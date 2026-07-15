import os, json
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.workflow.guard import check
from app.agents.workers.flight_worker import FlightWorker
from app.agents.workers.hotel_worker import HotelWorker
from app.agents.workers.attraction_worker import AttractionWorker
from app.agents.workers.itinerary_worker import ItineraryWorker
from app.agents.workers.budget_worker import BudgetWorker
from app.utils.llm import chat


WORKERS = {
    "flight": FlightWorker(),
    "hotel": HotelWorker(),
    "attraction": AttractionWorker(),
    "itinerary": ItineraryWorker(),
    "budget": BudgetWorker(),
}

WORKER_LIST = "flight(航班) hotel(酒店) attraction(景点) itinerary(日程) budget(预算)"


def _default_plan(msg: str) -> list[dict]:
    from_city, to_city = "出发地", "目的地"
    for c in ["上海","北京","深圳","广州","杭州","成都"]:
        if c in msg: from_city = c; break
    for c in ["东京","巴黎","曼谷","新加坡","伦敦","纽约","悉尼","迪拜","首尔"]:
        if c in msg: to_city = c; break
    return [
        {"id":1,"name":"查航班","worker":"flight","description":f"查{from_city}到{to_city}的航班","status":"pending","result":""},
        {"id":2,"name":"找酒店","worker":"hotel","description":f"找{to_city}的酒店","status":"pending","result":""},
        {"id":3,"name":"推荐景点","worker":"attraction","description":f"推荐{to_city}的热门景点","status":"pending","result":""},
        {"id":4,"name":"排日程","worker":"itinerary","description":f"排{to_city}每日日程","status":"pending","result":""},
        {"id":5,"name":"算预算","worker":"budget","description":f"汇总旅行预算","status":"pending","result":""},
    ]


async def guard_node(state: AgentState) -> AgentState:
    msg = state["messages"][-1]["content"]
    blocked, reason = check(msg)
    state["guard_blocked"] = blocked
    state["guard_reason"] = reason
    if blocked:
        state["final_answer"] = f"拒绝处理：{reason}"
    return state


async def planner_node(state: AgentState) -> AgentState:
    msg = state["messages"][-1]["content"]
    plan = _default_plan(msg)

    try:
        prompt = f"""可选Worker: {WORKER_LIST}
用户: {msg}
输出JSON数组(至少3项，每项含worker字段):
[{{"id":1,"name":"...","worker":"flight","description":"..."}}]
只输出JSON:"""
        resp = await chat([{"role":"user","content":prompt}])
        content = resp.get("content","").strip()
        s = content.find("["); e = content.rfind("]")
        if s != -1 and e != -1:
            llm_plan = json.loads(content[s:e+1])
            if isinstance(llm_plan, dict): llm_plan = list(llm_plan.values())
            llm_plan = [x for x in llm_plan if isinstance(x,dict) and "worker" in x and x["worker"] in WORKERS]
            if len(llm_plan) >= 3: plan = llm_plan
    except: pass

    state["plan_steps"] = plan
    state["current_step_index"] = 0
    print(f"[Planner] {len(plan)}步计划")
    return state


async def executor_node(state: AgentState) -> AgentState:
    steps = state.get("plan_steps",[])
    idx = state.get("current_step_index",0)
    if idx >= len(steps): return state
    step = steps[idx]
    w = WORKERS.get(step.get("worker",""))
    if not w: step["status"]="failed"; step["result"]="无对应Worker"; state["current_step_index"]+=1; return state

    print(f"[Executor] Step {idx+1}/{len(steps)}: {step['name']}")
    ctx = [{"step":s["name"],"result":s.get("result","")} for s in steps[:idx] if s.get("status")=="done"]
    step["status"]="running"
    try:
        step["result"] = await w.run(query=step.get("description",""), context=ctx if ctx else None)
        step["status"]="done"
    except Exception as e: step["result"]=str(e); step["status"]="failed"
    state["current_step_index"]+=1
    return state


async def aggregator_node(state: AgentState) -> AgentState:
    steps = state.get("plan_steps",[])
    msg = state["messages"][-1]["content"]
    text = "\n\n".join([f"Step{s['id']}[{s['name']}]:\n{s.get('result','')}" for s in steps])
    p = f"""汇总旅行方案。每个板块空行分隔。多用表格。

用户需求：{msg}
各步骤结果：{text}

输出方案："""
    r = await chat([{"role":"user","content":p}])
    state["final_answer"] = r.get("content","")
    return state


def route_guard(s): return "end" if s.get("guard_blocked") else "planner"
def route_executor(s): return "executor" if s.get("current_step_index",0) < len(s.get("plan_steps",[])) else "aggregator"

_graph=None
def build_graph():
    global _graph
    if _graph: return _graph
    g = StateGraph(AgentState)
    g.add_node("guard",guard_node)
    g.add_node("planner",planner_node)
    g.add_node("executor",executor_node)
    g.add_node("aggregator",aggregator_node)
    g.set_entry_point("guard")
    g.add_conditional_edges("guard",route_guard,{"end":END,"planner":"planner"})
    g.add_edge("planner","executor")
    g.add_conditional_edges("executor",route_executor,{"executor":"executor","aggregator":"aggregator"})
    g.add_edge("aggregator",END)
    _graph=g.compile()
    return _graph
