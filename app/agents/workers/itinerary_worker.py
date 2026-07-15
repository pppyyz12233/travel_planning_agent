"""日程 Worker —— MCP 天气 + RAG"""
from app.agents.workers.base import BaseWorker
from app.mcp.registry import ToolRegistry

class ItineraryWorker(BaseWorker):
    def __init__(self): super().__init__(name="itinerary")

    def _get_tools(self):
        all_tools = ToolRegistry.list_tools()
        return [t for t in all_tools
                if t["function"]["name"] in {"get_weather", "get_forecast"}]
