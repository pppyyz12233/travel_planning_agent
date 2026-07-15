"""Worker 基类 —— 读 SKILL.md + ReAct 循环。5 个 Worker 继承它。"""

import json
import os

from app.utils.llm import chat
from app.utils.config import MAX_TOOL_ITERATIONS
from app.mcp.registry import ToolRegistry


class BaseWorker:
    def __init__(self, name: str):
        self.name = name

        # 读 skills/{name}.md 作为 system prompt
        skill_path = f"app/agents/skills/{name}.md"
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = f"你是{name}专家。"

        self.max_iterations = MAX_TOOL_ITERATIONS

    async def run(self, query: str, context: list | None = None) -> str:
        """
        ReAct 循环：Thought → Action → Observation

        参数:
            query:   当前任务描述，如 "查上海到东京8月1日的航班"
            context: 前面步骤的结果 [{"step":"查航班","result":"MU523 2800元..."}, ...]
        返回:
            这个小弟的最终回答
        """
        # ── 构建初始消息 ──
        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            ctx_text = "前序步骤的结果：\n"
            for item in context:
                ctx_text += f"\n--- {item.get('step', '')} ---\n{item.get('result', '')}"
            messages.append({"role": "user", "content": ctx_text})

        messages.append({"role": "user", "content": query})

        # ── ReAct 循环 ──
        for i in range(self.max_iterations):
            print(f"  [{self.name}] 第{i+1}轮思考...")

            tools = self._get_tools() or None
            resp = await chat(messages, tools=tools)

            # AI 要调工具
            if resp.get("tool_calls"):
                tc = resp["tool_calls"][0]
                tool_name = tc.function.name
                try:
                    tool_args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                print(f"  [{self.name}] 调用工具: {tool_name}({tool_args})")

                observation = ToolRegistry.call(tool_name, **tool_args)
                print(f"  [{self.name}] 工具返回: {str(observation)[:100]}...")

                # 把工具调用和结果注入对话
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tc],
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(observation),
                })
            else:
                # AI 给最终答案
                print(f"  [{self.name}] ReAct 完成")
                return resp.get("content", "抱歉，无法回答。")

        # 兜底
        return "处理超时，请重试。"

    def _get_tools(self) -> list[dict]:
        """子类可重写，限定可用工具。默认返回全部。"""
        return ToolRegistry.list_tools()
