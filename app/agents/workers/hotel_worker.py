"""酒店 Worker —— MCP 酒店工具"""
from app.agents.workers.base import BaseWorker
from app.mcp.registry import ToolRegistry

class HotelWorker(BaseWorker):
    def __init__(self): super().__init__(name="hotel")

    def _get_tools(self):
        all_tools = ToolRegistry.list_tools()
        return [t for t in all_tools
                if t["function"]["name"] in {"search_hotels"}]
