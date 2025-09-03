def test_login_basic(page, base_url):
    page.goto(f"{base_url}/login")
    page.fill('#username', 'demo')
    page.fill('#password', 'mode')
    page.click('#submit')
    assert 'welcome' in (page.inner_text('#message') or '').lower()
