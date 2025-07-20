import uuid
from typing import Dict

from models import LoadedDocument

# Хранит id сессии, по которому доступен словарь с файлами, которые тоже доступны по id
store: Dict[uuid.UUID, Dict[uuid.UUID, LoadedDocument]] = {}


def save_document(session_id: uuid.UUID, document: LoadedDocument) -> uuid.UUID:
    file_id = uuid.uuid4()
    if session_id in store:
        store[session_id][file_id] = document
    else:
        store[session_id] = {file_id: document}

    return file_id


def get_document(session_id: uuid.UUID, document_id: uuid.UUID) -> LoadedDocument | None:
    session_documents = store.get(session_id, {})
    document = session_documents.get(document_id)

    return document


def get_documents(session_id: uuid.UUID) -> Dict[uuid.UUID, LoadedDocument]:
    return store.get(session_id, {})
