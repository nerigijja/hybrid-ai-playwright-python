from __future__ import annotations
from .base_page import BasePage
import yaml, pathlib
from core.ai.self_heal import SelfHealer, LocatorHint

class LoginPage(BasePage):
    def __init__(self, page, healer: SelfHealer):
        super().__init__(page, healer)
        # Load locators
        yml = yaml.safe_load(pathlib.Path('locators/login_page.yaml').read_text(encoding='utf-8'))['LoginPage']
        self.locators = {
            'username': LocatorHint(css=yml['username']['css'], attrs=yml['username'].get('attrs')),
            'password': LocatorHint(css=yml['password']['css'], attrs=yml['password'].get('attrs')),
            'submit':   LocatorHint(css=yml['submit']['css'],   attrs=yml['submit'].get('attrs')),
            'message':  LocatorHint(css=yml['message']['css'],  attrs=yml['message'].get('attrs')),
        }

    def fill_username(self, value: str):
        self.healer.query('LoginPage.username', self.locators['username']).fill(value)

    def fill_password(self, value: str):
        self.healer.query('LoginPage.password', self.locators['password']).fill(value)

    def submit(self):
        self.healer.query('LoginPage.submit', self.locators['submit']).click()

    def message_text(self) -> str:
        el = self.healer.query('LoginPage.message', self.locators['message'])
        return el.inner_text()
