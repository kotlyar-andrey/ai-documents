from typing import List

from langchain_core.vectorstores import InMemoryVectorStore
from langchain.schema import HumanMessage
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from config import EMBEDDING_MODEL, CHAT_MODEL, TEMPERATURE
from models import LoadedDocument

embedding = OpenAIEmbeddings(model=EMBEDDING_MODEL)
chat = ChatOpenAI(model=CHAT_MODEL, temperature=TEMPERATURE)


def get_embeddings(chunks: List[str]) -> InMemoryVectorStore:
    vector_store = InMemoryVectorStore.from_texts(chunks, embedding=embedding)
    return vector_store


async def get_document_summary(document: LoadedDocument) -> str:
    partial_summary = ""
    for text in document.chunks:
        prompt = f"Дай краткое, но информативное содержание следующего текста:\n{text}"
        response = await chat.ainvoke([HumanMessage(content=prompt)])
        partial_summary += response.content + "\n"

    final_prompt = (f"Вот краткое содержание отдельных частей документа:\n"
                    f"{partial_summary}\n"
                    f"Сделай итоговое краткое содержание для всего документа")
    result = await chat.ainvoke([HumanMessage(content=final_prompt)])

    return result.content
