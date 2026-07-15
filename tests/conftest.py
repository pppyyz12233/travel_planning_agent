"""测试 Fixtures"""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
