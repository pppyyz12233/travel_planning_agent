"""管理接口"""

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.auth.dependencies import require_admin
from app.crud import user, document

router = APIRouter(prefix="/admin", tags=["管理"])


#用户列表
@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    users = await user.list_users(db)
    return {
        "code": 200,
        "message": "",
        "data": [
            {"id": u.id, "username": u.username, "role": u.role, "created_at": str(u.created_at)}
            for u in users
        ]
    }


#设为管理员
@router.put("/users/{user_id}/promote")
async def promote(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    u = await user.set_admin(db, user_id)
    return {"code": 200, "message": "已设为管理员", "data": {"id": u.id, "username": u.username}}


#删除用户
@router.delete("/users/{user_id}")
async def delete(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    await user.delete_user(db, user_id)
    return {"code": 200, "message": "删除成功", "data": None}


#上传文档
@router.post("/upload")
async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    # 保存文件
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 解析文档
    text = handle_document(file_path)
    if not text:
        return {"code": 400, "message": "解析失败", "data": None}

    # 入库
    result = kb.upload_text(text, file.filename, operator=admin.username)
    doc = await document.add_document(
        db, admin.id, file.filename, file.filename.split(".")[-1], 0, []
    )

    return {"code": 200, "message": result, "data": {"document_id": doc.id, "filename": file.filename}}


#文档列表
@router.get("/documents")
async def list_docs(db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    docs = await document.list_documents(db)
    return {
        "code": 200,
        "message": "",
        "data": [
            {"id": d.id, "filename": d.filename, "file_type": d.file_type,
             "chunk_count": d.chunk_count, "created_at": str(d.created_at)}
            for d in docs
        ]
    }
