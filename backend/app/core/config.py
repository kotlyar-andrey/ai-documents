import os
import getpass
from typing import List
from dotenv import load_dotenv

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

ALLOWED_CONTENT_TYPES: List[str] = ['text/plain', 'application/pdf']

CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 50

EMBEDDING_MODEL: str = "text-embedding-3-small"
CHAT_MODEL: str = "gpt-4.1-nano"
MODERATION_MODEL: str = "omni-moderation-latest"
TEMPERATURE: float = 0.0
AMOUNT_OF_SIMILAR_CHUNKS: int = 3
