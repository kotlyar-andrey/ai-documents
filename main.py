import uuid
from typing import Annotated

from fastapi import FastAPI, UploadFile, Cookie, Response, HTTPException

from config import ALLOWED_FILE_TYPES
from models import Cookies, LoadedDocument, LoadDocumentResponse, SummaryResponse, ChatMessage
from utils import check_file_type, extract_text_from_file, split_text
from llm import get_embeddings, get_document_summary, moderate_message, get_relevant_embeddings, get_chat_answer
from storage import save_document, get_document, get_documents

app = FastAPI()


@app.get("/")
def index():
    return {"data": "Server is working"}


@app.post("/documents", response_model=LoadDocumentResponse)
async def load_document(file: UploadFile,
                        cookies: Annotated[Cookies, Cookie()],
                        response: Response):
    session_id = cookies.session_id if cookies.session_id else uuid.uuid4()
    if not check_file_type(file.filename):
        raise HTTPException(status_code=415,
                            detail=f"File type not allowed. Allowed file types: {ALLOWED_FILE_TYPES}")

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

    file_id = save_document(session_id, LoadedDocument(name=file.filename,
                                                       chunks=text_chunks,
                                                       embeddings=embeddings))

    response.set_cookie(key="session_id", value=str(session_id))

    return LoadDocumentResponse(message=f"Document '{file.filename}' was loaded", id=file_id)


@app.get("/documents/{document_id}/summary", response_model=SummaryResponse)
async def summary(document_id: uuid.UUID, cookies: Annotated[Cookies, Cookie()]):
    session_id = cookies.session_id
    if not session_id:
        raise HTTPException(status_code=401, detail="session_id was not found")

    document = get_document(session_id, document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document {document_id} was not found")

    try:
        result = await get_document_summary(document)
    except Exception as e:
        print(f"Logging an error in 'summary': {e}")
        raise HTTPException(status_code=503, detail="External server was not respond")

    return SummaryResponse(message=result)


@app.post("/chat", response_model=ChatMessage)
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

    relevant_embeddings = await get_relevant_embeddings(data.message, list(docs.values()))

    if len(relevant_embeddings) == 0:
        raise HTTPException(status_code=422, detail="Message isn't relevant to loaded documents")

    relevant_chunks = [doc[0].page_content for doc in relevant_embeddings]

    answer = await get_chat_answer(message, relevant_chunks)
    
    return ChatMessage(message=answer)
