import io, re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.finditer(r'onclick=([\"\'])(.*?)\1', html)
for m in matches:
    content = m.group(2)
    start_pos = max(0, m.start() - 30)
    end_pos = min(len(html), m.end() + 30)
    snippet = html[start_pos:end_pos].replace('\n', ' ')
    print(f"HANDLER: {content}")
    print(f"  SNIPPET: {snippet}")
