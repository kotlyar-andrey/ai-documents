from uuid import UUID
from typing import List

from pydantic import BaseModel, ConfigDict
from langchain_core.vectorstores import InMemoryVectorStore


class Cookies(BaseModel):
    session_id: UUID | None = None


class LoadedDocument(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    chunks: List[str]
    embeddings: InMemoryVectorStore


class LoadDocumentResponse(BaseModel):
    message: str
    id: UUID
