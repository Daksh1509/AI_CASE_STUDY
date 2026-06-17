# src/preprocess.py
"""Text cleaning and normalization utilities."""
import re
from typing import str

def remove_extra_whitespace(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def remove_special_chars(text: str, keep_punctuation: bool = True) -> str:
    if keep_punctuation:
        text = re.sub(r'[^\w\s.,!?;:\-\'"()]', ' ', text)
    else:
        text = re.sub(r'[^\w\s]', ' ', text)
    return text

def normalize_unicode(text: str) -> str:
    import unicodedata
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def remove_urls(text: str) -> str:
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def remove_emails(text: str) -> str:
    return re.sub(r'\S+@\S+\.\S+', '', text)

def clean_text(text: str, remove_urls_flag: bool = True,
               remove_emails_flag: bool = True,
               normalize: bool = True) -> str:
    """Full preprocessing pipeline."""
    if normalize:
        text = normalize_unicode(text)
    if remove_urls_flag:
        text = remove_urls(text)
    if remove_emails_flag:
        text = remove_emails(text)
    text = remove_special_chars(text)
    text = remove_extra_whitespace(text)
    return text

def clean_company_docs(docs: dict) -> dict:
    """Apply clean_text to a dict of {filename: raw_text}."""
    return {fname: clean_text(raw) for fname, raw in docs.items()}
