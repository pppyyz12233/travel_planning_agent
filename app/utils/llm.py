"""DeepSeek API 封装 —— 全项目唯一调 LLM 的地方"""

from openai import AsyncOpenAI
from app.utils.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)


async def chat(messages: list[dict], tools: list[dict] | None = None) -> dict:
    """
    给 DeepSeek 发一轮消息，拿回复。

    参数:
        messages: [{"role":"user","content":"你好"}]
        tools:    OpenAI Function Calling 格式的工具列表

    返回:
        {"content": "AI的回复", "tool_calls": [...]}
        - 如果 AI 直接回答，tool_calls 为空
        - 如果 AI 要调工具，content 为空，tool_calls 有内容
    """
    params = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.3,
    }
    if tools:
        params["tools"] = tools

    try:
        response = await client.chat.completions.create(**params)
    except Exception:
        import asyncio
        await asyncio.sleep(1)
        response = await client.chat.completions.create(**params)

    msg = response.choices[0].message
    return {
        "content": msg.content or "",
        "tool_calls": msg.tool_calls or [],
    }


async def chat_stream(messages: list[dict]) -> str:
    """流式输出，一个字一个字往外蹦（前端用）"""
    stream = await client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        temperature=0.3,
        stream=True,
    )
    result = ""
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            result += chunk.choices[0].delta.content
    return result
