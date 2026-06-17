# src/references.py
"""Extract URLs and citations from raw text."""
import re
from typing import List, Dict

URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`]+')
DOI_PATTERN = re.compile(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b', re.IGNORECASE)

def extract_urls(text: str) -> List[str]:
    """Return all HTTP/HTTPS URLs found in text."""
    return list(set(URL_PATTERN.findall(text)))

def extract_dois(text: str) -> List[str]:
    """Return all DOI references found in text."""
    return list(set(DOI_PATTERN.findall(text)))

def extract_all_references(text: str) -> Dict[str, List[str]]:
    """Return a dict with urls and dois."""
    return {
        "urls": extract_urls(text),
        "dois": extract_dois(text),
    }

def flatten_references(refs: Dict[str, List[str]]) -> List[str]:
    """Flatten the reference dict into a single list."""
    flat = []
    for items in refs.values():
        flat.extend(items)
    return flat

def extract_refs_all_docs(docs: dict) -> dict:
    """Extract references for every document in a company dict."""
    return {fname: flatten_references(extract_all_references(text))
            for fname, text in docs.items()}
