"""消息数据操作"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


#添加消息
async def add_message(db: AsyncSession, conversation_id: int, role: str, content: str):
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


#对话历史
async def get_history(db: AsyncSession, conversation_id: int):
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    return list(result.scalars().all())
