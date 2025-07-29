from typing import List

from app.core.config import ALLOWED_CONTENT_TYPES, CHUNK_OVERLAP, CHUNK_SIZE
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def check_file_type(content_type: str | None) -> bool:
    for file_type in ALLOWED_CONTENT_TYPES:
        if content_type == file_type:
            return True
    return False


async def extract_text_from_file(file: UploadFile) -> str:
    if file.content_type == "text/plain":
        content = await file.read()
        return content.decode("utf-8")
    elif file.content_type == "application/pdf":
        pdf = PdfReader(file.file)
        return "\n".join([page.extract_text() for page in pdf.pages])

    raise TypeError(f"Only {ALLOWED_CONTENT_TYPES} file types allowed")


def split_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_text(text)
    return chunks
