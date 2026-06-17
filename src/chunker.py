# src/chunker.py
"""Sliding-window text chunker with token overlap."""
from typing import List
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping word-level chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start += chunk_size - overlap
    return chunks

def chunk_by_sentences(text: str, max_sentences: int = 10) -> List[str]:
    """Split text into groups of sentences."""
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunks.append(" ".join(sentences[i:i + max_sentences]))
    return chunks

def chunk_documents(docs: dict, strategy: str = "words") -> dict:
    """Chunk all documents in a company dict."""
    chunked = {}
    for fname, text in docs.items():
        if strategy == "sentences":
            chunked[fname] = chunk_by_sentences(text)
        else:
            chunked[fname] = chunk_text(text)
    return chunked
