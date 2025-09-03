from __future__ import annotations
import argparse, pathlib, os, re, sys
from difflib import get_close_matches

KEYWORD_MAP = {
    'open': 'open_url',
    'go to': 'open_url',
    'type': 'type_text',
    'enter': 'type_text',
    'click': 'click',
    'press': 'press',
    'expect text': 'should_see_text',
    'see': 'should_see_text',
}

TEMPLATE = '''import pytest
from keywords.web_keywords import Keywords

def test_generated(page, base_url, healer):
    kw = Keywords(page, base_url, healer)
{steps}
'''

def to_step(line: str) -> str:
    s = line.strip().rstrip('.')
    if not s: return ''
    # naive parse
    m = re.match(r'^(open|go to)\s+(.+)$', s, flags=re.I)
    if m:
        return f"    kw.open_url('{m.group(2)}')"
    m = re.match(r'^(click|press)\s+(.+)$', s, flags=re.I)
    if m:
        return f"    kw.click('{m.group(2)}')"
    m = re.match(r'^(type|enter)\s+(.+?)\s+into\s+(.+)$', s, flags=re.I)
    if m:
        return f"    kw.type_text('{m.group(3)}', '{m.group(2)}')"
    m = re.match(r'^(expect|see)\s+(.+)$', s, flags=re.I)
    if m:
        return f"    kw.should_see_text('{m.group(2)}')"
    # fallback: fuzzy choose a keyword by verb
    verb = s.split()[0].lower()
    chosen = get_close_matches(verb, list(KEYWORD_MAP.keys()), n=1)
    api = KEYWORD_MAP.get(chosen[0], 'noop') if chosen else 'noop'
    return f"    kw.{api}('{s}')  # TODO: verify parsing"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('steps_file', help='Plain text/markdown with one step per line')
    ap.add_argument('--out', default='tests/generated/test_from_steps.py')
    args = ap.parse_args()
    lines = pathlib.Path(args.steps_file).read_text(encoding='utf-8').splitlines()
    body = '\n'.join(filter(None, (to_step(l) for l in lines)))
    out = TEMPLATE.format(steps=body if body else '    pass')
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding='utf-8')
    print(f'Generated: {out_path}')

if __name__ == '__main__':
    main()
