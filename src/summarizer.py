# src/summarizer.py
"""Summarization using HuggingFace transformers (BART)."""
from typing import List
from src.config import SUMMARIZER_MODEL

_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        from transformers import pipeline
        _pipeline = pipeline("summarization", model=SUMMARIZER_MODEL)
    return _pipeline

def summarize_chunk(text: str, max_length: int = 150,
                    min_length: int = 40) -> str:
    """Summarize a single text chunk."""
    if len(text.split()) < min_length:
        return text
    pipe = get_pipeline()
    result = pipe(text, max_length=max_length,
                  min_length=min_length, do_sample=False)
    return result[0]["summary_text"]

def summarize_chunks(chunks: List[str], max_length: int = 150) -> List[str]:
    """Summarize a list of chunks."""
    return [summarize_chunk(c, max_length=max_length) for c in chunks]

def summarize_document(text: str, chunk_size: int = 512) -> str:
    """End-to-end: chunk -> summarize -> join."""
    from src.chunker import chunk_text
    chunks = chunk_text(text, chunk_size=chunk_size)
    summaries = summarize_chunks(chunks)
    return " ".join(summaries)

def summarize_all_docs(docs: dict) -> dict:
    """Summarize all documents in a {filename: text} dict."""
    return {fname: summarize_document(text) for fname, text in docs.items()}
