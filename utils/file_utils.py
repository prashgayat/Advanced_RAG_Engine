import os
import tempfile
from typing import Tuple

from PyPDF2 import PdfReader
import docx
import pandas as pd

# Create a temp folder for saving uploaded files
TEMP_DIR = tempfile.gettempdir()

def save_uploaded_file(uploaded_file) -> str:
    """
    Saves the uploaded file to a temporary directory and returns its saved path.
    """
    save_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def load_file_content(file_path: str) -> Tuple[str, str]:
    """
    Loads and extracts text content from the saved file.
    Returns a tuple: (content, file_type).
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path), "pdf"
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path), "docx"
    elif file_extension == ".txt":
        return extract_text_from_txt(file_path), "txt"
    elif file_extension == ".xlsx":
        return extract_text_from_xlsx(file_path), "xlsx"
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_xlsx(file_path: str) -> str:
    df = pd.read_excel(file_path)
    return df.to_string(index=False)

