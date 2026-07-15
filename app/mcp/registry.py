"""MCP 工具注册表 —— Worker 通过它发现和调用工具"""

from app.mcp.servers.flight_server import search_flights, get_flight_price
from app.mcp.servers.hotel_server import search_hotels
from app.mcp.servers.weather_server import get_weather, get_forecast
from app.mcp.servers.exchange_server import get_exchange_rate


class ToolRegistry:
    _tools = {}  # {工具名: (函数, 描述, 参数定义)}

    @classmethod
    def register(cls, name: str, func, description: str, parameters: dict = None):
        cls._tools[name] = (func, description, parameters or {})

    @classmethod
    def list_tools(cls) -> list[dict]:
        """返回 OpenAI Function Calling 格式，含参数定义，LLM 才知道参数叫什么"""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": desc,
                    "parameters": params,
                },
            }
            for name, (_, desc, params) in cls._tools.items()
        ]

    @classmethod
    def call(cls, name: str, **kwargs) -> str:
        func, _, _ = cls._tools[name]
        result = func(**kwargs)
        if isinstance(result, (list, dict)):
            return str(result)
        return str(result)


def init_registry():
    ToolRegistry.register(
        "search_flights", search_flights,
        "搜索航班",
        {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "出发城市（中文名或三字码，如 上海/SHA）"},
                "destination": {"type": "string", "description": "目的城市（中文名或三字码，如 东京/TYO）"},
                "date": {"type": "string", "description": "日期，格式 YYYY-MM-DD"},
            },
            "required": ["origin", "destination"],
        },
    )
    ToolRegistry.register(
        "get_flight_price", get_flight_price,
        "查询航班价格",
        {
            "type": "object",
            "properties": {
                "flight_id": {"type": "string", "description": "航班号，如 MU523"},
            },
            "required": ["flight_id"],
        },
    )
    ToolRegistry.register(
        "search_hotels", search_hotels,
        "搜索酒店",
        {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名"},
                "budget": {"type": "string", "enum": ["low", "mid", "high", "all"],
                           "description": "预算档位：low/mid/high/all"},
            },
            "required": ["city"],
        },
    )
    ToolRegistry.register(
        "get_weather", get_weather,
        "查询城市当前天气",
        {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称（英文，如 Tokyo、Paris）"},
            },
            "required": ["city"],
        },
    )
    ToolRegistry.register(
        "get_forecast", get_forecast,
        "查询城市未来几天天气预报",
        {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称（英文）"},
                "days": {"type": "integer", "description": "预报天数，默认3天"},
            },
            "required": ["city"],
        },
    )
    ToolRegistry.register(
        "get_exchange_rate", get_exchange_rate,
        "查询汇率",
        {
            "type": "object",
            "properties": {
                "from_currency": {"type": "string", "description": "源货币代码（CNY/USD/JPY/EUR等）"},
                "to_currency": {"type": "string", "description": "目标货币代码"},
            },
        },
    )
