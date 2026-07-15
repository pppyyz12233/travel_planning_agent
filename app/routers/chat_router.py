"""对话接口"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.auth.dependencies import get_current_user
from app.schemas.chat import ChatRequest
from app.agents.workflow.guard import check
from app.agents.supervisor import build_graph
from app.crud import conversation, message

router = APIRouter(prefix="/chat", tags=["对话"])


@router.post("")
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Guard
    blocked, reason = check(req.message)
    if blocked:
        return {"code": 403, "message": reason, "data": None}

    # 获取或创建对话
    conv_id = req.conversation_id
    if not conv_id:
        conv = await conversation.create_conversation(db, user.id, req.message[:30])
        conv_id = conv.id

    # 加载历史消息作为上下文（长期记忆）
    history_messages = []
    if req.conversation_id:
        msgs = await message.get_history(db, conv_id)
        for m in msgs[-20:]:  # 最多20条历史
            history_messages.append({"role": m.role, "content": m.content})

    # 构建 Agent 输入
    state = {
        "messages": history_messages + [{"role": "user", "content": req.message}],
        "plan_steps": [],
        "current_step_index": 0,
        "final_answer": "",
        "guard_blocked": False,
        "guard_reason": "",
        "need_clarify": False,
        "clarify_question": "",
    }

    result = await build_graph().ainvoke(state)

    # 保存本轮对话
    await message.add_message(db, conv_id, "user", req.message)
    await message.add_message(db, conv_id, "assistant", result["final_answer"])

    return {
        "code": 200,
        "message": "",
        "data": {
            "conversation_id": conv_id,
            "reply": result["final_answer"],
        }
    }


@router.get("/history")
async def history(conversation_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    msgs = await message.get_history(db, conversation_id)
    return {
        "code": 200,
        "message": "",
        "data": [
            {"id": m.id, "role": m.role, "content": m.content, "created_at": str(m.created_at)}
            for m in msgs
        ]
    }


@router.get("/conversations")
async def conversations(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    convs = await conversation.list_by_user(db, user.id)
    return {
        "code": 200,
        "message": "",
        "data": [
            {"id": c.id, "title": c.title, "created_at": str(c.created_at)}
            for c in convs
        ]
    }
