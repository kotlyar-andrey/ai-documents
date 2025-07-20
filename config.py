from typing import List
from dotenv import load_dotenv

load_dotenv()

ALLOWED_FILE_TYPES: List[str] = ['.pdf', '.txt']

CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 50

EMBEDDING_MODEL: str = "text-embedding-3-small"
