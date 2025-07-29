from typing import Annotated

from app.core.db import get_documents
from app.models import ChatMessage, Cookies
from app.services.openai import (
    get_chat_answer,
    get_relevant_embeddings,
    moderate_message,
)
from fastapi import APIRouter, Cookie, HTTPException

router = APIRouter(prefix="/chat")


@router.post("/", response_model=ChatMessage)
async def chat(data: ChatMessage, cookies: Annotated[Cookies, Cookie()]):
    message = data.message

    session_id = cookies.session_id
    if not session_id:
        raise HTTPException(status_code=401, detail="session_id was not found")

    docs = get_documents(session_id)
    if not docs:
        raise HTTPException(status_code=404, detail="Documents was not found")

    is_message_flagged = await moderate_message(data.message)
    if is_message_flagged:
        raise HTTPException(status_code=422, detail="Message has inappropriate content")

    relevant_embeddings = await get_relevant_embeddings(
        data.message, list(docs.values())
    )

    if len(relevant_embeddings) == 0:
        raise HTTPException(
            status_code=422, detail="Message isn't relevant to loaded documents"
        )

    relevant_chunks = [doc[0].page_content for doc in relevant_embeddings]

    answer = await get_chat_answer(message, relevant_chunks)

    return ChatMessage(message=answer)
    return ChatMessage(message=answer)
    answer = await get_chat_answer(message, relevant_chunks)

    return ChatMessage(message=answer)
    return ChatMessage(message=answer)
