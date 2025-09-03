from typing import Dict, List, Any
import textwrap, pathlib, json
from loguru import logger

def generate_manual_testcases(analysis: Dict[str, Any], out_path: str = 'artifacts/manual_testcases.md'):
    lines = []
    lines.append(f"# Manual Testcases for {analysis.get('url')}")
    lines.append('')
    lines.append(f"Title: {analysis.get('title')}")
    lines.append('')
    tc_id = 1
    for form in analysis.get('forms', []):
        lines.append(f"## Testcases for form: {form.get('id')}")
        for inp in form.get('inputs', []):
            lines.append(f"### TC-{tc_id:03d} - Verify {inp.get('label') or inp.get('name') or inp.get('placeholder') or inp.get('id') or inp.get('type')}")
            lines.append('**Steps:**')
            lines.append(f"1. Open the application URL: {analysis.get('url')}")
            lines.append(f"2. Locate the field: {inp.get('label') or inp.get('name') or inp.get('placeholder') or inp.get('id')}")
            lines.append('3. Enter valid input and submit the form.')
            lines.append('4. Verify expected success message or next page loads.')
            lines.append('**Expected Result:**')
            lines.append('Appropriate success behavior or navigation.')
            lines.append('')
            tc_id += 1
    # Add button tests
    for btn in analysis.get('buttons', []):
        lines.append(f"### TC-{tc_id:03d} - Verify button: {btn.get('text') or btn.get('selector')}")
        lines.append('**Steps:**')
        lines.append(f"1. Open the application URL: {analysis.get('url')}")
        lines.append(f"2. Click the button: {btn.get('text') or btn.get('selector')}")
        lines.append('3. Verify expected behavior (navigation, popup, form submission)')
        lines.append('**Expected Result:**')
        lines.append('Button behaves as expected.')
        lines.append('')
        tc_id += 1

    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines), encoding='utf-8')
    logger.info(f"Manual testcases written to {p}")
    return str(p)

def generate_automation_tests(analysis: Dict[str, Any], out_path: str = 'tests/generated/test_from_ui.py', base_url_placeholder: str = None):
    # Build pytest file using keywords/web_keywords and executables/pages where possible
    lines = []
    lines.append('import pytest')
    lines.append('from keywords.web_keywords import Keywords')
    lines.append('')
    lines.append("def test_generated_from_ui(page, base_url, healer):")
    lines.append("    kw = Keywords(page, base_url, healer)")
    lines.append("    # Auto-generated steps from UI analysis")
    # simple mapping: open URL, fill fields from first form, click first button
    lines.append(f"    kw.open_url('')  # use base_url or full path as needed")
    if analysis.get('forms'):
        form = analysis['forms'][0]
        for inp in form.get('inputs'):
            # choose selector preference
            sel = inp.get('id') or inp.get('name') or inp.get('placeholder') or inp.get('data-testid') or inp.get('class') or ''
            # translate to a locator expression acceptable by keywords.type_text
            if sel:
                if '=' in sel or sel.startswith('#') or sel.startswith('.'):
                    locator = sel
                else:
                    # assume id or name
                    locator = f'#{sel}' if not sel.startswith('#') else sel
            else:
                locator = inp.get('label') or inp.get('placeholder') or ''
            lines.append(f"    kw.type_text('{locator}', '<<AUTO_INPUT>>')  # field: {inp.get('name') or inp.get('label')}")
        # click submit/button if exists
        if analysis.get('buttons'):
            btn = analysis['buttons'][0]
            lines.append(f"    kw.click('{btn.get('text') or btn.get('selector')}')")
    else:
        # fallback: click first button
        if analysis.get('buttons'):
            btn = analysis['buttons'][0]
            lines.append(f"    kw.click('{btn.get('text') or btn.get('selector')}')")
    lines.append("    # TODO: replace <<AUTO_INPUT>> with realistic test data and assertions")


    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines), encoding='utf-8')
    return str(p)
