from playwright.sync_api import sync_playwright
from loguru import logger
from typing import Dict, List, Any
import re, time, json

def _clean(s: str):
    return (s or '').strip()

def analyze_url(url: str, timeout: int = 5000) -> Dict[str, Any]:
    """Navigate to `url` and return a structured description of interactive UI elements."""
    logger.info(f"Analyzing UI: {url}")
    result = {'url': url, 'title': '', 'forms': [], 'buttons': [], 'links': [], 'texts': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=timeout)
        time.sleep(0.5)
        result['title'] = page.title()
        # Collect forms
        forms = page.query_selector_all('form')
        for idx, f in enumerate(forms):
            try:
                fid = f.get_attribute('id') or f.get_attribute('name') or f.get_attribute('action') or f.get_attribute('data-testid') or f.get_attribute('class') or f.get_attribute('role') or f.get_attribute('aria-label')
                inputs = []
                for inp in f.query_selector_all('input,textarea,select'):
                    inputs.append({
                        'tag': inp.evaluate('el => el.tagName.toLowerCase()'),
                        'type': inp.get_attribute('type') or '',
                        'name': inp.get_attribute('name') or '',
                        'id': inp.get_attribute('id') or '',
                        'placeholder': inp.get_attribute('placeholder') or '',
                        'label': _extract_label_text(page, inp),
                        'required': True if inp.get_attribute('required') is not None else False,
                        'data-testid': inp.get_attribute('data-testid') or '',
                        'class': inp.get_attribute('class') or ''
                    })
                result['forms'].append({'id': fid or f'form_{idx}', 'inputs': inputs})
            except Exception:
                continue

        # Buttons
        for b in page.query_selector_all('button, input[type=submit], [role=button]'):
            try:
                text = _clean(b.inner_text())
                sel = _unique_selector(page, b)
                result['buttons'].append({'text': text, 'selector': sel})
            except Exception:
                continue

        # Links
        for a in page.query_selector_all('a[href]'):
            try:
                text = _clean(a.inner_text())
                href = a.get_attribute('href') or ''
                sel = _unique_selector(page, a)
                result['links'].append({'text': text, 'href': href, 'selector': sel})
            except Exception:
                continue

        # Text nodes (common headings and paragraphs to assert)
        for tag in ['h1','h2','h3','p','label']:
            for el in page.query_selector_all(tag):
                try:
                    txt = _clean(el.inner_text())
                    if txt and len(txt) < 200:
                        sel = _unique_selector(page, el)
                        result['texts'].append({'tag': tag, 'text': txt, 'selector': sel})
                except Exception:
                    continue

        context.close()
        browser.close()
    return result

def _extract_label_text(page, inp):
    try:
        # look for <label for="id">
        idv = inp.get_attribute('id')
        if idv:
            lab = page.query_selector_all(f'label[for="{idv}"]')
            if lab:
                return lab[0].inner_text().strip()
        # look for parent label
        parent = inp.evaluate_handle('el => el.closest("label")')
        if parent:
            return parent.as_element().inner_text().strip()
    except Exception:
        pass
    return ''

def _unique_selector(page, el):
    # Try data-testid, id, name, aria-label, role, then fallback to xpath
    try:
        tid = el.get_attribute('data-testid') or el.get_attribute('id') or el.get_attribute('name') or el.get_attribute('aria-label') or el.get_attribute('role')
        if tid:
            if ' ' in tid:
                return f'text="{el.inner_text().strip()}"'
            if el.get_attribute('id'):
                return f'#{el.get_attribute("id")}'
            if el.get_attribute('data-testid'):
                return f'[data-testid="{el.get_attribute("data-testid")}"]'
            return f'[{tid}]'
        # fallback xpath using element index snippet
        idx = page.query_selector_all('*').index(el) if False else None
    except Exception:
        pass
    # ultimate fallback: use text() if available
    try:
        txt = el.inner_text().strip()
        if txt:
            return f'text="{txt}"'
    except Exception:
        pass
    # last resort: return empty, caller must handle
    return ''

if __name__ == '__main__':
    import sys, json
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
    out = analyze_url(url)
    print(json.dumps(out, indent=2))
