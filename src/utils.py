# src/utils.py
"""General-purpose utilities: logging, directory helpers, timestamps."""
import os
import logging
from pathlib import Path
from datetime import datetime
from src.config import LOG_LEVEL

# ── Logging setup ───────────────────────────────────────
def get_logger(name: str = "ai_case_study") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    return logger

logger = get_logger()

# ── Directory helpers ──────────────────────────────────
def ensure_dir(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def list_files(directory: str, extensions=(".txt", ".pdf", ".docx")):
    result = []
    for root, _, files in os.walk(directory):
        for f in files:
            if Path(f).suffix.lower() in extensions:
                result.append(os.path.join(root, f))
    return result

# ── Timestamp helpers ─────────────────────────────────
def get_timestamp(fmt: str = "%Y%m%d_%H%M%S") -> str:
    return datetime.now().strftime(fmt)

def timestamped_filename(base_name: str, ext: str = "md") -> str:
    return f"{base_name}_{get_timestamp()}.{ext}"

# ── Text helpers ────────────────────────────────────
def truncate(text: str, max_chars: int = 500) -> str:
    return text[:max_chars] + "..." if len(text) > max_chars else text

def word_count(text: str) -> int:
    return len(text.split())
