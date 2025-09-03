import os, base64, html
from datetime import datetime

class HtmlReport:
    def __init__(self, title='Test Report'):
        self.title = title
        self.generated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        self.tests = []
        self.meta = {}

    def add_meta(self, key, value):
        self.meta[key] = value

    def add_test_result(self, name, outcome, duration=0.0, message=None, screenshot_path=None, artifacts=None):
        entry = {
            'name': name,
            'outcome': outcome,
            'duration': duration,
            'message': message or '',
            'artifacts': artifacts or [],
            'screenshot_base64': None
        }
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                entry['screenshot_base64'] = base64.b64encode(f.read()).decode('utf-8')
        self.tests.append(entry)

    def generate_html(self, output='test-report.html'):
        lines = ['<html><head><meta charset="utf-8"/></head><body>']
        lines.append(f'<h2>{html.escape(self.title)}</h2><div>{self.generated_at}</div>')
        if self.meta:
            lines.append("<h3>Meta Information</h3><ul>")
            for k, v in self.meta.items():
                lines.append(f"<li><b>{html.escape(str(k))}</b>: {html.escape(str(v))}</li>")
            lines.append("</ul>")
        lines.append('<table border=1 cellpadding=5><tr><th>Test</th><th>Outcome</th><th>Duration</th><th>Message</th></tr>')
        for t in self.tests:
            lines.append(f"<tr><td>{html.escape(t['name'])}</td><td>{html.escape(t['outcome'])}</td><td>{t['duration']:.2f}</td><td>{html.escape(t['message'] or '')}</td></tr>")
        lines.append('</table></body></html>')
        with open(output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return output
