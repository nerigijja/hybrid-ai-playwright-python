"""CLI entrypoint: given a URL, analyze the UI, create manual testcases (markdown),
and generate an automation pytest using the keyword layer.

Usage:
    python -m core.ai.auto_from_url <url> [--out-tests tests/generated/test_from_ui.py]
"""
from core.ai.ui_analyzer import analyze_url
from core.ai.testcase_generator import generate_manual_testcases, generate_automation_tests
import argparse, json, pathlib, os, sys
from loguru import logger

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url', help='Environment URL to analyze')
    ap.add_argument('--out-tests', default='tests/generated/test_from_ui.py')
    ap.add_argument('--out-manual', default='artifacts/manual_testcases.md')
    args = ap.parse_args()
    logger.info(f"Starting UI analysis for: {args.url}")
    analysis = analyze_url(args.url)
    # persist raw analysis
    pathlib.Path('artifacts').mkdir(exist_ok=True)
    pathlib.Path('artifacts/ui_analysis.json').write_text(json.dumps(analysis, indent=2), encoding='utf-8')
    manual = generate_manual_testcases(analysis, args.out_manual)
    auto = generate_automation_tests(analysis, args.out_tests)
    print('Manual testcases ->', manual)
    print('Generated tests ->', auto)

if __name__ == '__main__':
    main()
