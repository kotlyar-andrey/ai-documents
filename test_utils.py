import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from tempfile import SpooledTemporaryFile

from utils import check_file_type, extract_text_from_file, split_text


@pytest.fixture
def mock_upload_file():
    mock_file = AsyncMock()
    return mock_file


def test_check_file_type():
    """Проверка типов файлов"""
    good_file_names = ['test.pdf', 'test.txt']
    bad_file_names = ['test.png', 'test.doc', 'test.jpg']

    for name in good_file_names:
        assert check_file_type(name)

    for name in bad_file_names:
        assert not check_file_type(name)


@pytest.mark.asyncio
async def test_extract_text_valid_txt(mock_upload_file):
    """Успешное чтение текстового файла"""
    good_text = "Some test text".encode("utf-8")
    mock_upload_file.filename = "good.txt"
    mock_upload_file.read.return_value = good_text
    result = await extract_text_from_file(mock_upload_file)

    assert result == "Some test text"


@pytest.mark.asyncio
async def test_extract_text_invalid_txt(mock_upload_file):
    """Ошибка чтения текстового файла, например, из-за неправильной кодировки"""
    bad_text = "кириллица".encode("cp1251")
    mock_upload_file.filename = "bad.txt"
    mock_upload_file.read.return_value = bad_text

    with pytest.raises(UnicodeDecodeError):
        await extract_text_from_file(mock_upload_file)


@pytest.mark.asyncio
@patch("utils.PdfReader")
@patch("utils.SpooledTemporaryFile")
async def test_extract_text_valid_pdf(mock_spooled_file, mock_pdf_reader, mock_upload_file):
    """Успешное чтение pdf файла """
    mock_upload_file.filename = "test.pdf"
    mock_upload_file.read.return_value = b'Some content'

    tmp_file = MagicMock(spec=SpooledTemporaryFile)
    mock_spooled_file.return_value = tmp_file

    page1 = MagicMock()
    page1.extract_text.return_value = "text from page 1"
    page2 = MagicMock()
    page2.extract_text.return_value = "text from page 2"

    pdf = MagicMock()
    pdf.pages = [page1, page2]
    mock_pdf_reader.return_value = pdf

    result = await extract_text_from_file(mock_upload_file)

    assert result == "text from page 1\ntext from page 2"
    tmp_file.write.assert_called_once_with(b'Some content')
    mock_pdf_reader.assert_called_once_with(tmp_file)


@pytest.mark.asyncio
@patch("utils.PdfReader")
@patch("utils.SpooledTemporaryFile")
async def test_extract_text_invalid_pdf(mock_spooled_file, mock_pdf_reader, mock_upload_file):
    """Ошибка чтения pdf файла """
    mock_upload_file.filename = "test.pdf"
    mock_upload_file.read.return_value = b'Some content'

    mock_spooled_file_instance = MagicMock()
    mock_spooled_file.return_value = mock_spooled_file_instance

    mock_pdf_reader.side_effect = Exception("Error message")

    with pytest.raises(Exception, match="Error message"):
        await extract_text_from_file(mock_upload_file)


@patch("utils.RecursiveCharacterTextSplitter")
def test_split_text(mock_recursive_splitter):
    text = "Some text"

    mock_recursive_splitter.return_value.split_text.return_value = ["Some", "text"]

    result = split_text(text)

    mock_recursive_splitter.assert_called_once()
    mock_recursive_splitter.return_value.split_text.assert_called_once_with(text)
    assert result == ["Some", "text"]
