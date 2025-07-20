import io

from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": "Server is working"}


@patch("main.uuid.uuid4")
@patch("main.check_file_type")
@patch("main.extract_text_from_file")
def test_load_document_ok(mock_extract_text_from_file, mock_check_file_type, mock_uuid4):
    mock_check_file_type.return_value = True
    mock_extract_text_from_file.return_value = "Some text"
    mock_uuid4.return_value = "11111111-1111-1111-1111-111111111111"

    response = client.post("/documents",
                           files={"file": ("test.pdf", io.BytesIO(b"Some text"), "application/pdf")})

    assert response.status_code == 200
    assert response.json() == {"data": "Some text"}
    assert response.cookies.get("session_id") == "11111111-1111-1111-1111-111111111111"


@patch("main.uuid.uuid4")
@patch("main.check_file_type")
@patch("main.extract_text_from_file")
def test_load_document_bad_file_type(mock_extract_text_from_file, mock_check_file_type, mock_uuid4):
    mock_check_file_type.return_value = False
    mock_extract_text_from_file.return_value = "Some text"
    mock_uuid4.return_value = "11111111-1111-1111-1111-111111111111"

    response = client.post("/documents",
                           files={"file": ("test.err", io.BytesIO(b"Some text"), "application/pdf")})

    assert response.status_code == 400
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

    assert response.status_code == 400
    assert response.json().get("detail") == "Cant read the file"


