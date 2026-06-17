# src/input_loader.py
"""Load raw input files: PDF, DOCX, TXT."""
import os
from pathlib import Path
from typing import List, Dict

def load_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_pdf(filepath: str) -> str:
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text
    except ImportError:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")

def load_docx(filepath: str) -> str:
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])
    except ImportError:
        raise ImportError("python-docx not installed. Run: pip install python-docx")

def load_file(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    loaders = {".pdf": load_pdf, ".docx": load_docx, ".txt": load_txt}
    if ext not in loaders:
        raise ValueError(f"Unsupported file type: {ext}")
    return loaders[ext](filepath)

def load_company_folder(folder_path: str) -> Dict[str, str]:
    """Load all supported files from a company folder."""
    result = {}
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if Path(fpath).suffix.lower() in (".pdf", ".docx", ".txt"):
            result[fname] = load_file(fpath)
    return result

def load_all_companies(raw_dir: str) -> Dict[str, Dict[str, str]]:
    """Recursively load all company folders inside raw_dir."""
    companies = {}
    for company in os.listdir(raw_dir):
        folder = os.path.join(raw_dir, company)
        if os.path.isdir(folder):
            companies[company] = load_company_folder(folder)
    return companies
