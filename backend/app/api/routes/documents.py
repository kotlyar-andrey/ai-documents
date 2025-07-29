import uuid
from typing import Annotated

from app.core.config import ALLOWED_CONTENT_TYPES
from app.core.db import delete_document, get_document, get_documents, save_document
from app.models import (
    Cookies,
    GetAllDocumentsResponse,
    LoadDocumentResponse,
    LoadedDocument,
    SummaryResponse,
)
from app.services.openai import get_document_summary, get_embeddings
from app.utils import check_file_type, extract_text_from_file, split_text
from fastapi import APIRouter, Cookie, HTTPException, Response, UploadFile

router = APIRouter(prefix="/documents")


@router.get("/", response_model=GetAllDocumentsResponse)
async def get_all_documents(cookies: Annotated[Cookies, Cookie()], response: Response):
    session_id = cookies.session_id if cookies.session_id else uuid.uuid4()
    docs = get_documents(session_id)

    response.set_cookie(key="session_id", value=str(session_id), domain="localhost")

    return GetAllDocumentsResponse(
        documents=[
            LoadDocumentResponse(id=id_, name=doc.name) for id_, doc in docs.items()
        ]
    )


@router.post("/", response_model=LoadDocumentResponse)
async def load_document(
    file: UploadFile, cookies: Annotated[Cookies, Cookie()], response: Response
):
    session_id = cookies.session_id if cookies.session_id else uuid.uuid4()
    if not check_file_type(file.content_type):
        raise HTTPException(
            status_code=415,
            detail=f"File type not allowed. Allowed files: {ALLOWED_CONTENT_TYPES}",
        )

    try:
        text = await extract_text_from_file(file)
    except Exception as e:
        print(f"Logging an error in 'load_document': {e}")
        raise HTTPException(status_code=422, detail="Cant read the file")

    text_chunks = split_text(text)

    try:
        embeddings = get_embeddings(text_chunks)
    except Exception as e:
        print(f"Logging an error in 'load_document': {e}")
        raise HTTPException(status_code=503, detail="External server was not respond")

    file_id = save_document(
        session_id,
        LoadedDocument(name=file.filename, chunks=text_chunks, embeddings=embeddings),
    )

    response.set_cookie(key="session_id", value=str(session_id), domain="localhost")

    return LoadDocumentResponse(
        message=f"Document '{file.filename}' was loaded", id=file_id, name=file.filename
    )


@router.get("/{document_id}/summary", response_model=SummaryResponse)
async def summary(document_id: uuid.UUID, cookies: Annotated[Cookies, Cookie()]):
    session_id = cookies.session_id
    if not session_id:
        raise HTTPException(status_code=401, detail="session_id was not found")

    document = get_document(session_id, document_id)
    if not document:
        raise HTTPException(
            status_code=404, detail=f"Document {document_id} was not found"
        )

    try:
        result = await get_document_summary(document)
    except Exception as e:
        print(f"Logging an error in 'summary': {e}")
        raise HTTPException(status_code=503, detail="External server was not respond")

    return SummaryResponse(message=result)


@router.delete("/{document_id}")
async def remove_document(
    document_id: uuid.UUID, cookies: Annotated[Cookies, Cookie()]
):
    session_id = cookies.session_id
    if not session_id:
        raise HTTPException(status_code=401, detail="session_id was not found")

    delete_document(session_id, document_id)
    delete_document(session_id, document_id)
