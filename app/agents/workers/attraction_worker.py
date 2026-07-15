"""景点 Worker —— 纯LLM推理，不依赖RAG"""
from app.agents.workers.base import BaseWorker

class AttractionWorker(BaseWorker):
    def __init__(self): super().__init__(name="attraction")

    def _get_tools(self):
        return []  # 无MCP工具，纯LLM推理