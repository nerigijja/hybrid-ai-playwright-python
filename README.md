# Hybrid Playwright + Python Test Framework (with AI helpers)

A pragmatic hybrid framework combining **Keyword-driven**, **Data-driven**, and **POM** (Page Object Model) patterns — plus "AI-inspired" helpers for:
- **Self-healing locators** (heuristic similarity matching when selectors break)
- **Natural language → test steps** generator (maps plain English to keywords; optional LLM plug)
- **Smart assertions** (fuzzy text/visual checks)
- **Flake guard** (auto-rerun + instability hints)

> Works out-of-the-box without external AI keys. If you provide `OPENAI_API_KEY`, the generator can use an LLM (optional).

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
pytest -q
```

## Run a keyword test from natural language

```bash
# Example: convert steps.md into a real pytest file using fuzzy mapping (and OpenAI if key is set)
python -m core.ai.generator steps.md --out tests/generated/test_from_steps.py
pytest -q tests/generated/test_from_steps.py
```

## Structure

- `pages/`: Page Objects (POM)
- `keywords/`: high-level reusable actions (keyword-driven)
- `data/`: test data files (data-driven)
- `core/ai/`: self-healing, generator, assertions, flaky utilities
- `locators/`: YAML-based locators and fallbacks
- `config/config.yaml`: environment & runtime config
- `conftest.py`: Pytest fixtures (browser/page, config, logger, healer)
- `tools/dom_snapshot.py`: optional DOM dump for debugging

## Self-healing overview
1. Try primary selector.
2. If it fails, score candidate elements in the DOM against known attributes (text, role, data-testid, class, id) via fuzzy similarity.
3. If top score ≥ threshold (default 0.72), use it and **persist** the new selector suggestion to the healing cache (`.artifacts/self_heal.json`).

## Notes
- This repo ships with an example `LoginPage` and a sample test.
- Keep selectors in `locators/*.yaml` to gain healing automatically.
- To turn features on/off, see `config/config.yaml`.


## Auto UI analysis & test generation

You can auto-generate manual testcases and automation scripts from a live environment URL:

```bash
python -m core.ai.auto_from_url https://your-app.example.com --out-tests tests/generated/test_from_ui.py --out-manual artifacts/manual_testcases.md
```

This will create:
- `artifacts/ui_analysis.json` (raw UI analysis)
- `artifacts/manual_testcases.md` (human-readable manual testcases)
- a pytest file under `tests/generated/` ready for refinement.

The generator uses heuristics to pick input selectors and buttons; review and replace `<<AUTO_INPUT>>` tokens with realistic data and add assertions.
