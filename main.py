import uuid
from typing import Annotated

from fastapi import FastAPI, UploadFile, Cookie, Response, HTTPException

from config import ALLOWED_FILE_TYPES
from models import Cookies, LoadedDocument, LoadDocumentResponse
from utils import check_file_type, extract_text_from_file, split_text
from llm import get_embeddings
from storage import save_document

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
