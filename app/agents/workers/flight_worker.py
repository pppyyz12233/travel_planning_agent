"""航班 Worker —— MCP 航班工具"""
from app.agents.workers.base import BaseWorker
from app.mcp.registry import ToolRegistry

class FlightWorker(BaseWorker):
    def __init__(self): super().__init__(name="flight")

    def _get_tools(self):
        """只暴露航班相关工具"""
        all_tools = ToolRegistry.list_tools()
        return [t for t in all_tools
                if t["function"]["name"] in {"search_flights", "get_flight_price"}]
