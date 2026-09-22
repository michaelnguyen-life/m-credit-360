import io, re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.finditer(r'onclick=([\"\'])(.*?)\1', html)
with io.open('all_onclicks.txt', 'w', encoding='utf-8') as out:
    for idx, m in enumerate(matches):
        content = m.group(2)
        start_pos = max(0, m.start() - 40)
        end_pos = min(len(html), m.end() + 40)
        snippet = html[start_pos:end_pos].replace('\n', ' ')
        out.write(f"[{idx:2d}] {content}\n     SNIPPET: {snippet}\n")

print("Wrote all_onclicks.txt")
