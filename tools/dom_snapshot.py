from playwright.sync_api import Page

def dump_dom(page: Page, path='dom.html'):
    html = page.content()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path
