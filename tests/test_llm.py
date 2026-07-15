"""LLM 层测试"""

import pytest
from app.utils.llm import chat


@pytest.mark.asyncio
async def test_chat_normal():
    """测试：正常对话"""
    resp = await chat([{"role": "user", "content": "回复一个OK，不要其他内容"}])
    assert resp["content"] is not None
    assert "OK" in resp["content"] or "ok" in resp["content"].lower()


@pytest.mark.asyncio
async def test_chat_no_tools():
    """测试：无工具时 tool_calls 为空"""
    resp = await chat([{"role": "user", "content": "你好"}])
    assert resp["tool_calls"] == [] or resp["tool_calls"] is None


@pytest.mark.asyncio
async def test_chat_with_tools():
    """测试：传工具列表不报错"""
    tools = [{"type": "function", "function": {"name": "test", "description": "测试"}}]
    resp = await chat([{"role": "user", "content": "你好"}], tools=tools)
    assert resp["content"] or resp["tool_calls"] is not None
