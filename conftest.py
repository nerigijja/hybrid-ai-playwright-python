import os, pathlib, pytest
from core.config import Config
from core.logger import init_logger
from core.ai.self_heal import SelfHealer
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='session')
def cfg():
    return Config('config/config.yaml')

@pytest.fixture(scope='session')
def artifacts(tmp_path_factory):
    d = pathlib.Path('.artifacts')
    d.mkdir(exist_ok=True, parents=True)
    return d

@pytest.fixture(scope='session', autouse=True)
def _log(artifacts):
    init_logger(artifacts)

@pytest.fixture(scope='session')
def base_url(cfg):
    return cfg.base_url

@pytest.fixture(scope='session')
def browser_name(cfg):
    return cfg.get('browser')

@pytest.fixture(scope='session')
def _browser_context_args(cfg, artifacts):
    args = {}
    if cfg.get('video') == 'on':
        args['record_video_dir'] = str(artifacts / 'video')
    return args

@pytest.fixture(scope='session')
def playwright_context(cfg, browser_name, _browser_context_args):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=cfg.get('headless'), slow_mo=cfg.get('slowmo_ms'))
        context = browser.new_context(**_browser_context_args)
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()

@pytest.fixture
def healer(cfg, page):
    return SelfHealer(page, threshold=cfg.get('ai','heal_threshold'), persist=cfg.get('ai','persist_suggestions'))
