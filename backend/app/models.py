from typing import List
from uuid import UUID

from langchain_core.vectorstores import InMemoryVectorStore
from pydantic import BaseModel, ConfigDict


class Cookies(BaseModel):
    session_id: UUID | None = None


class LoadedDocument(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str | None
    chunks: List[str]
    embeddings: InMemoryVectorStore


class ChatMessage(BaseModel):
    message: str


class LoadDocumentResponse(BaseModel):
    message: str | None = None
    id: UUID
    name: str | None


class GetAllDocumentsResponse(BaseModel):
    documents: List[LoadDocumentResponse]


class SummaryResponse(BaseModel):
    message: str
