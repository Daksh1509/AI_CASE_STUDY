# src/insight_extractor.py
"""Extract structured insights from summarized text."""
import re
from typing import Dict, List

INSIGHT_KEYWORDS = {
    "problem": ["challenge", "problem", "issue", "pain point", "difficulty"],
    "solution": ["solution", "approach", "implement", "deploy", "integrate"],
    "result": ["result", "outcome", "impact", "achieve", "improve", "reduce", "increase"],
    "technology": ["AI", "ML", "cloud", "data", "platform", "model", "algorithm"],
    "industry": ["finance", "healthcare", "retail", "manufacturing", "logistics"],
}

def score_sentence(sentence: str) -> Dict[str, float]:
    """Score a sentence against each insight category."""
    sentence_lower = sentence.lower()
    scores = {}
    for category, keywords in INSIGHT_KEYWORDS.items():
        scores[category] = sum(1 for kw in keywords if kw.lower() in sentence_lower)
    return scores

def extract_insights(text: str, top_n: int = 5) -> Dict[str, List[str]]:
    """Extract top sentences per category."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    categorized: Dict[str, List[tuple]] = {k: [] for k in INSIGHT_KEYWORDS}
    for sent in sentences:
        scores = score_sentence(sent)
        for category, score in scores.items():
            if score > 0:
                categorized[category].append((score, sent.strip()))
    result = {}
    for category, scored_sents in categorized.items():
        top = sorted(scored_sents, key=lambda x: x[0], reverse=True)[:top_n]
        result[category] = [s for _, s in top]
    return result

def extract_from_all_docs(docs: dict) -> dict:
    """Run insight extraction on each document summary."""
    return {fname: extract_insights(text) for fname, text in docs.items()}
