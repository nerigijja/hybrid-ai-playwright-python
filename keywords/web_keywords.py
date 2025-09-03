from __future__ import annotations
from core.ai.assertions import fuzzy_contains
from loguru import logger

class Keywords:
    def __init__(self, page, base_url, healer):
        self.page = page
        self.base_url = base_url.rstrip('/')
        self.healer = healer

    def open_url(self, url: str):
        if not (url.startswith('http://') or url.startswith('https://')):
            url = f"{self.base_url}/{url.lstrip('/')}"
        logger.info(f"Open URL: {url}")
        self.page.goto(url, wait_until='domcontentloaded')

    def click(self, text_or_selector: str):
        # Try text first, then CSS
        try:
            self.page.get_by_text(text_or_selector, exact=False).first.click(timeout=1000)
        except Exception:
            self.page.locator(text_or_selector).first.click()

    def type_text(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def should_see_text(self, expected: str, tolerance=0.75):
        body = self.page.locator('body').inner_text()
        ok, score = fuzzy_contains(body, expected, tolerance=tolerance)
        assert ok, f"Expected fuzzy text '{expected}' not found (score={score:.2f})"

    def press(self, key: str):
        self.page.keyboard.press(key)

    def noop(self, text: str):
        logger.warning(f"No-op for step: {text}")
