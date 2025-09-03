import pytest
from playwright.sync_api import sync_playwright
import os
from executables.api.api_client import APIClient
from executables.db.db_client import DBClient
from util.html_report import HtmlReport

def pytest_addoption(parser):
    parser.addoption('--base-url', action='store', default='https://example.com', help='base url')
    parser.addoption('--headed', action='store_true', help='run headed')

@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption('--base-url')

@pytest.fixture(scope='session')
def api_client(base_url):
    return APIClient(base_url + "/api")

@pytest.fixture(scope='session')
def db_client():
    db = DBClient(os.path.join(os.getcwd(), 'data', 'test.db'))
    yield db
    db.close()

@pytest.fixture(scope='function')
def page(request, base_url):
    headed = request.config.getoption('--headed')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

# ---------------- HTML Reporting ----------------
REPORT_PATH = os.environ.get('HTML_REPORT_PATH', 'artifacts/test-report.html')
os.makedirs('artifacts', exist_ok=True)
_reporter = HtmlReport('Hybrid Test Run')
_reporter.add_meta('base_url', os.environ.get('BASE_URL','https://example.com'))

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call':
        name = item.nodeid
        outcome_str = 'passed' if rep.passed else ('skipped' if rep.skipped else 'failed')
        duration = getattr(rep, 'duration', 0.0) if hasattr(rep, 'duration') else 0.0
        message = ''
        if rep.failed:
            try:
                message = str(rep.longrepr)
            except:
                message = repr(rep.longrepr)
        screenshot_path = None
        try:
            page = item.funcargs.get('page')
            if page:
                safe = name.replace('::','__').replace('/','_')
                screenshot_path = os.path.join('artifacts', f"{safe}.png")
                page.screenshot(path=screenshot_path, full_page=True)
        except Exception:
            screenshot_path = None
        artifacts = []
        if screenshot_path:
            artifacts.append(screenshot_path)
        _reporter.add_test_result(name=name, outcome=outcome_str, duration=duration, message=message, screenshot_path=screenshot_path, artifacts=artifacts)

def pytest_sessionfinish(session, exitstatus):
    _reporter.generate_html(REPORT_PATH)
    print(f'[reporter] HTML report written to {REPORT_PATH}')
