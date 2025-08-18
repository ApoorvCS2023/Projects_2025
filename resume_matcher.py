# resume_matcher.py
# Lightweight matcher that uses Amazon Comprehend for key-phrase extraction
# and simple token-overlap scoring to avoid heavy ML deps in Lambda.

import re
import json
from typing import List, Dict, Tuple
import boto3

# Comprehend client (available in Lambda runtime)
comprehend = boto3.client("comprehend")

# Basic stopwords to reduce noise; keep it small to avoid false negatives
STOPWORDS = {
    "a","an","the","and","or","of","for","to","in","on","with","by","at","from",
    "as","is","are","be","being","been","that","this","it","its","you","your",
    "we","our","us"
}

def _normalize_space(s: str) -> str:
    # lower + collapse whitespace
    return re.sub(r"\s+", " ", s.strip().lower())

def _clean_phrase(p: str) -> str:
    # drop outer punctuation; keep internal symbols like +, -, &
    p = _normalize_space(p)
    p = re.sub(r"^[^\w]+|[^\w]+$", "", p)
    return p

def _tokenize(s: str) -> List[str]:
    # split on non-word boundaries; filter stopwords and very short tokens
    toks = re.findall(r"[a-zA-Z0-9\+\.\-]+", s.lower())
    return [t for t in toks if t not in STOPWORDS and len(t) > 1]

def _dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _chunk(text: str, max_chars: int = 4500) -> List[str]:
    # Comprehend has input size limits; chunk by characters safely
    text = text or ""
    if len(text) <= max_chars:
        return [text]
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i:i+max_chars])
        i += max_chars
    return chunks

def aws_extract_key_phrases(text: str) -> List[str]:
    # Call Comprehend across chunks and merge phrases
    phrases: List[str] = []
    for chunk in _chunk(text):
        resp = comprehend.detect_key_phrases(Text=chunk, LanguageCode="en")
        for kp in resp.get("KeyPhrases", []):
            phrases.append(_clean_phrase(kp.get("Text", "")))
    # Filter short/empty and dedupe
    phrases = [p for p in phrases if p and len(p.split()) <= 6]
    return _dedupe_preserve_order(phrases)

def _jaccard(a_tokens: List[str], b_tokens: List[str]) -> float:
    a, b = set(a_tokens), set(b_tokens)
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0

def _best_pairs(res_phrases: List[str], jd_phrases: List[str], top_k: int = 10) -> List[Tuple[str, str, float]]:
    pairs: List[Tuple[str, str, float]] = []
    jd_tok = [(p, _tokenize(p)) for p in jd_phrases]
    for rp in res_phrases:
        rtok = _tokenize(rp)
        best_score, best_jp = 0.0, ""
        for jp, jtok in jd_tok:
            score = _jaccard(rtok, jtok)
            if score > best_score:
                best_score, best_jp = score, jp
        if best_score > 0.0:
            pairs.append((rp, best_jp, best_score))
    # sort desc by score and keep top_k
    pairs.sort(key=lambda x: x[2], reverse=True)
    return pairs[:top_k]

def _coverage(jd_phrases: List[str], res_phrases: List[str], thresh: float = 0.6) -> float:
    jd_tok = [_tokenize(p) for p in jd_phrases]
    res_tok = [_tokenize(p) for p in res_phrases]
    if not jd_tok:
        return 0.0
    hits = 0
    for jt in jd_tok:
        best = 0.0
        for rt in res_tok:
            best = max(best, _jaccard(jt, rt))
        if best >= thresh:
            hits += 1
    return hits / len(jd_tok)

def generate_match_report(jd_text: str, resume_text: str) -> Dict:
    """
    Main entry: extract phrases via Comprehend, score overlap, and return JSON-safe dict.
    """
    jd_phrases = aws_extract_key_phrases(jd_text)
    resume_phrases = aws_extract_key_phrases(resume_text)

    pairs = _best_pairs(resume_phrases, jd_phrases, top_k=10)
    cov = _coverage(jd_phrases, resume_phrases, thresh=0.6)
    # Scale coverage to a 0..100 score
    overall = round(cov * 100, 2)

    return {
        "overall_match_score": overall,            # percentage
        "jd_key_phrases": jd_phrases[:50],         # cap for response size
        "resume_key_phrases": resume_phrases[:50],
        "top_matches": [
            {"resume_phrase": r, "jd_phrase": j, "score": round(s, 2)}
            for (r, j, s) in pairs
        ]
    }
