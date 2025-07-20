import uuid
from typing import Annotated

from fastapi import FastAPI, UploadFile, Cookie, Response, HTTPException

from config import ALLOWED_FILE_TYPES
from models import Cookies
from utils import check_file_type, extract_text_from_file

app = FastAPI()


@app.get("/")
def index():
    return {"data": "Server is working"}


@app.post("/documents")
async def load_document(file: UploadFile,
                        cookies: Annotated[Cookies, Cookie()],
                        response: Response):
    session_id = cookies.session_id if cookies.session_id else uuid.uuid4()
    if not check_file_type(file.filename):
        raise HTTPException(status_code=400,
                            detail=f"File type not allowed. Allowed file types: {ALLOWED_FILE_TYPES}")

    try:
        text = await extract_text_from_file(file)
    except Exception as e:
        print(f"Logging an error in 'load_document': {e}")
        raise HTTPException(status_code=400, detail="Cant read the file")

    response.set_cookie(key="session_id", value=str(session_id))

    return {"data": text}
