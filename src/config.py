# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

# ── Model Settings ────────────────────────────────────────
SUMMARIZER_MODEL   = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
GENERATOR_MODEL    = os.getenv("GENERATOR_MODEL",  "gpt-3.5-turbo")
EMBEDDING_MODEL    = os.getenv("EMBEDDING_MODEL",  "all-MiniLM-L6-v2")

# ── Chunking ──────────────────────────────────────────────
CHUNK_SIZE         = int(os.getenv("CHUNK_SIZE",    "512"))
CHUNK_OVERLAP      = int(os.getenv("CHUNK_OVERLAP", "64"))

# ── Paths ─────────────────────────────────────────────────
RAW_DATA_DIR       = os.getenv("RAW_DATA_DIR",  "data/raw")
CLEAN_DATA_DIR     = os.getenv("CLEAN_DATA_DIR","data/cleaned")
OUTPUT_DIR         = os.getenv("OUTPUT_DIR",    "outputs")
CASE_STUDY_DIR     = os.path.join(OUTPUT_DIR, "case_studies")
SUMMARY_DIR        = os.path.join(OUTPUT_DIR, "summaries")
EVIDENCE_DIR       = os.path.join(OUTPUT_DIR, "evidence")
SCREENSHOT_DIR     = os.path.join(OUTPUT_DIR, "screenshots")

# ── Logging ───────────────────────────────────────────────
LOG_LEVEL          = os.getenv("LOG_LEVEL", "INFO")
