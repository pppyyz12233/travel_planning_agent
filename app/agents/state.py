"""Agent 状态定义 —— 所有节点共享"""

from typing import TypedDict


class AgentState(TypedDict):
    messages: list[dict]            # 对话历史
    plan_steps: list[dict]          # [{id, name, worker, description, status, result}]
    current_step_index: int         # 当前执行到第几步
    final_answer: str               # 汇总后的最终回复
    guard_blocked: bool             # 安全门卫是否拦截
    guard_reason: str               # 拦截原因