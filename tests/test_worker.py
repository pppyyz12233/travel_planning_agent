"""Worker ReAct 测试"""

import pytest
from app.mcp.registry import init_registry
from app.agents.workers.flight_worker import FlightWorker
from app.agents.workers.hotel_worker import HotelWorker
from app.agents.workers.attraction_worker import AttractionWorker

init_registry()


@pytest.mark.asyncio
async def test_flight_worker():
    """测试：航班 Worker ReAct 循环"""
    worker = FlightWorker()
    result = await worker.run("查上海到东京的航班")
    assert len(result) > 20
    assert "MU" in result or "航班" in result


@pytest.mark.asyncio
async def test_hotel_worker():
    """测试：酒店 Worker"""
    worker = HotelWorker()
    result = await worker.run("找东京的中档酒店")
    assert len(result) > 10


@pytest.mark.asyncio
async def test_attraction_worker():
    """测试：景点 Worker"""
    worker = AttractionWorker()
    result = await worker.run("推荐东京的景点")
    assert len(result) > 10


@pytest.mark.asyncio
async def test_worker_with_context():
    """测试：带上下文的 Worker"""
    worker = FlightWorker()
    context = [{"step": "查航班", "result": "MU523 2800元"}]
    result = await worker.run("有没有更便宜的", context=context)
    assert len(result) > 5
