from __future__ import annotations
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, Any, Optional
from loguru import logger
import json, pathlib
import re

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or '').strip().lower())

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()

@dataclass
class LocatorHint:
    css: Optional[str] = None
    attrs: Optional[Dict[str, str]] = None

class SelfHealer:
    def __init__(self, page, threshold: float = 0.72, persist: bool = True, cache_dir: str = ".artifacts"):
        self.page = page
        self.threshold = threshold
        self.persist = persist
        self.cache_path = pathlib.Path(cache_dir) / "self_heal.json"
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.cache_path.exists():
            self.cache_path.write_text("{}", encoding="utf-8")

    def _save_suggestion(self, key: str, selector: str):
        if not self.persist:
            return
        try:
            data = json.loads(self.cache_path.read_text(encoding='utf-8'))
        except Exception:
            data = {}
        data[key] = selector
        self.cache_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        logger.debug(f"Healed selector stored: {key} -> {selector}")

    def query(self, key: str, hint: LocatorHint):
        # 1) Try cache
        try:
            cache = json.loads(self.cache_path.read_text(encoding='utf-8'))
            if key in cache:
                sel = cache[key]
                loc = self.page.locator(sel)
                if loc.count() > 0:
                    logger.debug(f"Using cached healed locator for {key}: {sel}")
                    return loc
        except Exception:
            pass

        # 2) Try primary CSS chain
        if hint.css:
            loc = self.page.locator(hint.css)
            if loc.count() > 0:
                return loc

        # 3) Self-heal by scanning candidates
        attrs = hint.attrs or {}
        candidates = self.page.locator("*")  # all elements
        n = min(200, candidates.count())
        best = (0.0, None, None)  # (score, locator_str, element_handle)
        for i in range(n):
            el = candidates.nth(i)
            try:
                # Build a simple signature of the element
                txt = (el.inner_text(timeout=50) or "").strip()
                role = (el.get_attribute("role") or "")
                testid = (el.get_attribute("data-testid") or "")
                eid = (el.get_attribute("id") or "")
                cls = (el.get_attribute("class") or "")
                sig = f"text={txt}|role={role}|testid={testid}|id={eid}|class={cls}"
                score = 0.0
                for k,v in attrs.items():
                    if k == 'role':
                        score = max(score, similarity(role, v))
                    elif k == 'data-testid':
                        score = max(score, similarity(testid, v))
                    else:
                        score = max(score, similarity(sig, f"{k}={v}"))
                # If no attrs provided, fall back to text similarity
                if not attrs:
                    score = similarity(txt, "".join([v for v in [txt, role, testid] if v]))
                if score > best[0]:
                    # Build a robust selector proposal
                    proposal = None
                    if testid:
                        proposal = f"[data-testid=\"{testid}\"]"
                    elif eid:
                        proposal = f"#{eid}"
                    elif role and txt:
                        proposal = f"role={role} >> text={txt}"
                    elif txt:
                        proposal = f"text={txt}"
                    else:
                        # last resort: nth-of-type (brittle)
                        proposal = f"xpath=(//*[@class][{i+1}])"
                    best = (score, proposal, el)
            except Exception:
                continue

        score, selector, el = best
        if score >= self.threshold and selector:
            logger.info(f"[SELF-HEAL] {key} healed with score={score:.2f} -> {selector}")
            self._save_suggestion(key, selector)
            return self.page.locator(selector)

        raise LookupError(f"Unable to locate element for {key}; best_score={score:.2f}")
