from typing import List

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from config import EMBEDDING_MODEL

embedding = OpenAIEmbeddings(model=EMBEDDING_MODEL)


def get_embeddings(chunks: List[str]) -> InMemoryVectorStore:
    vector_store = InMemoryVectorStore.from_texts(chunks, embedding=embedding)
    return vector_store
