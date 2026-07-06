"""知识库检索 Schema"""

from pydantic import BaseModel


class ChunkItem(BaseModel):
    content: str
    score: float
    source: str  # 文档文件名


class SearchResult(BaseModel):
    query: str
    chunks: list[ChunkItem]
