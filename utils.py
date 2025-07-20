from tempfile import SpooledTemporaryFile
from typing import List

from fastapi import UploadFile
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import ALLOWED_FILE_TYPES, CHUNK_SIZE, CHUNK_OVERLAP


def check_file_type(filename: str) -> bool:
    for file_type in ALLOWED_FILE_TYPES:
        if filename.lower().endswith(file_type):
            return True
    return False


async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return content.decode("utf-8")
    elif filename.endswith(".pdf"):
        tmp_file = SpooledTemporaryFile()
        tmp_file.write(content)
        pdf = PdfReader(tmp_file)
        return "\n".join([page.extract_text() for page in pdf.pages])

    raise TypeError(f"Only {ALLOWED_FILE_TYPES} file types allowed")


def split_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_text(text)
    return chunks
