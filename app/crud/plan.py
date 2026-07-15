"""计划数据操作"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan


#创建计划
async def create_plan(db: AsyncSession, user_id: int, title: str, steps: list):
    plan = Plan(user_id=user_id, title=title, steps=steps, status="running")
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


#更新计划状态
async def update_status(db: AsyncSession, plan_id: int, status: str):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    if plan:
        plan.status = status
        await db.commit()
    return plan


#用户计划列表
async def list_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Plan).where(Plan.user_id == user_id).order_by(Plan.created_at.desc())
    )
    return list(result.scalars().all())
