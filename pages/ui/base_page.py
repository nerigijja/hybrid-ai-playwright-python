from __future__ import annotations
from loguru import logger

class BasePage:
    def __init__(self, page, healer):
        self.page = page
        self.healer = healer

    def go(self, url: str):
        logger.info(f"Navigate: {url}")
        return self.page.goto(url, wait_until='domcontentloaded')
