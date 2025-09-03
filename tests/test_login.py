import pytest
from pages.ui.login_page import LoginPage
from util.data_loader import load_data
from core.ai.assertions import fuzzy_contains

@pytest.mark.parametrize("creds", load_data("data/users.json"))
def test_sample_login(page, base_url, healer, creds):
    lp = LoginPage(page, healer)
    lp.go(base_url)
    # Example usage with JSON data
    # lp.fill_username(creds["username"])
    # lp.fill_password(creds["password"])
    # lp.submit()
    # msg = lp.message_text()
    # ok, score = fuzzy_contains(msg, "welcome", tolerance=0.6)
    # assert ok, f"Login message too dissimilar (score={score:.2f})"
    assert page.title()  # placeholder assertion
