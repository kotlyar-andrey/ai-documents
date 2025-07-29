from typing import List

from app.core.config import (
    AMOUNT_OF_SIMILAR_CHUNKS,
    CHAT_MODEL,
    EMBEDDING_MODEL,
    MODERATION_MODEL,
    TEMPERATURE,
)
from app.models import LoadedDocument
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

embedding = OpenAIEmbeddings(model=EMBEDDING_MODEL)
chat = ChatOpenAI(model=CHAT_MODEL, temperature=TEMPERATURE)
client = OpenAI()


def get_embeddings(chunks: List[str]) -> InMemoryVectorStore:
    vector_store = InMemoryVectorStore.from_texts(texts=chunks, embedding=embedding)
    return vector_store


async def get_document_summary(document: LoadedDocument) -> str:
    partial_summary: str = ""
    for text in document.chunks:
        prompt = f"Дай краткое, но информативное содержание следующего текста:\n{text}"
        response = await chat.ainvoke([HumanMessage(content=prompt)])
        partial_summary += str(response.content) + "\n"

    final_prompt = (
        f"Вот краткое содержание отдельных частей документа:\n"
        f"{partial_summary}\n"
        f"Сделай итоговое краткое содержание для всего документа"
    )
    result = await chat.ainvoke([HumanMessage(content=final_prompt)])

    return str(result.content)


async def moderate_message(message: str) -> bool:
    response = client.moderations.create(input=message, model=MODERATION_MODEL)
    result = response.results[0]
    return result.flagged


async def get_message_embedding(message: str) -> List[float]:
    result = await embedding.aembed_query(message)
    return result


async def get_relevant_embeddings(
    message: str, docs: List[LoadedDocument]
) -> list[tuple[Document, float]]:
    message_embedding = await get_message_embedding(message)

    all_relevant_embeddings = []
    for doc in docs:
        doc_embeddings = doc.embeddings.similarity_search_with_score_by_vector(
            embedding=message_embedding, k=AMOUNT_OF_SIMILAR_CHUNKS
        )

        all_relevant_embeddings.extend(
            [(d, score) for d, score in doc_embeddings if score > 0.3]
        )

    all_relevant_embeddings.sort(key=lambda emb: emb[1], reverse=True)

    relevant_embeddings = all_relevant_embeddings[:AMOUNT_OF_SIMILAR_CHUNKS]

    return relevant_embeddings


async def get_chat_answer(message: str, chunks: List[str]) -> str:
    system_prompt = f"Ты AI ассистент, который отвечает на вопросы пользователя, \
    основываясь только на информации, предоставленной ниже. Если ответа в этой \
    информации нет, так и скажи, не придумывай информациию и не пользуйся собственными \
    знаниями. Предоставленная информация:\n{'\n'.join(chunks)}"

    result = await chat.ainvoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=message)]
    )

    return str(result.content)
    return str(result.content)
