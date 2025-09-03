from __future__ import annotations
from loguru import logger
from PIL import Image
import imagehash, io

def fuzzy_contains(actual: str, expected: str, tolerance: float = 0.75):
    a = (actual or '').strip().lower()
    b = (expected or '').strip().lower()
    # simple token-based match
    hits = sum(1 for t in b.split() if t in a)
    score = hits / max(1, len(b.split()))
    logger.debug(f"Fuzzy text score={score:.2f} (expect≥{tolerance}) | expected='{expected}' actual='{actual}'")
    return score >= tolerance, score

def visual_similar(img_bytes_a: bytes, img_bytes_b: bytes, cutoff: int = 8):
    A = Image.open(io.BytesIO(img_bytes_a)).convert('L')
    B = Image.open(io.BytesIO(img_bytes_b)).convert('L')
    ha = imagehash.phash(A)
    hb = imagehash.phash(B)
    dist = ha - hb
    return dist <= cutoff, int(dist)
