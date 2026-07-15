"""预算 Worker —— MCP 汇率工具"""
from app.agents.workers.base import BaseWorker
from app.mcp.registry import ToolRegistry

class BudgetWorker(BaseWorker):
    def __init__(self): super().__init__(name="budget")

    def _get_tools(self):
        all_tools = ToolRegistry.list_tools()
        return [t for t in all_tools
                if t["function"]["name"] in {"get_exchange_rate"}]
