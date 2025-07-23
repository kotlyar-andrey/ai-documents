import io
import uuid

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from llm import InMemoryVectorStore

from main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": "Server is working"}


@patch("main.uuid.uuid4")
@patch("main.check_file_type")
@patch("main.extract_text_from_file")
@patch("main.split_text")
@patch("main.get_embeddings")
@patch("main.save_document")
def test_load_document_ok(mock_save_document, mock_get_embedding, mock_split_text,
                          mock_extract_text_from_file, mock_check_file_type, mock_uuid4):
    mock_session_id = "11111111-1111-1111-1111-111111111111"
    mock_file_id = "22222222-2222-2222-2222-222222222222"
    mock_check_file_type.return_value = True
    mock_extract_text_from_file.return_value = "Some text"
    mock_split_text.return_value = ['text chunk 1', 'text chunk 2']
    mock_get_embedding.return_value = MagicMock(spec=InMemoryVectorStore)
    mock_save_document.return_value = mock_file_id
    mock_uuid4.return_value = mock_session_id

    response = client.post("/documents",
                           files={"file": ("test.pdf", io.BytesIO(b"Some text"), "application/pdf")})

    assert response.status_code == 200
    assert response.json() == {'id': mock_file_id, 'name': 'test.pdf', 'message': "Document 'test.pdf' was loaded"}


@patch("main.uuid.uuid4")
@patch("main.check_file_type")
@patch("main.extract_text_from_file")
def test_load_document_bad_file_type(mock_extract_text_from_file, mock_check_file_type, mock_uuid4):
    mock_check_file_type.return_value = False
    mock_extract_text_from_file.return_value = "Some text"
    mock_uuid4.return_value = "11111111-1111-1111-1111-111111111111"

    response = client.post("/documents",
                           files={"file": ("test.err", io.BytesIO(b"Some text"), "application/pdf")})

    assert response.status_code == 415
    assert "File type not allowed" in response.json().get("detail")


@patch("main.uuid.uuid4")
@patch("main.check_file_type")
@patch("main.extract_text_from_file")
def test_load_document_bad_file_type(mock_extract_text_from_file, mock_check_file_type, mock_uuid4):
    mock_check_file_type.return_value = True
    mock_extract_text_from_file.side_effect = UnicodeDecodeError
    mock_uuid4.return_value = "11111111-1111-1111-1111-111111111111"

    response = client.post("/documents",
                           files={"file": ("test.err", io.BytesIO(b"Some text"), "application/pdf")})

    assert response.status_code == 422
    assert response.json().get("detail") == "Cant read the file"
