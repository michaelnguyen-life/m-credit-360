import io
import re
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<input[^>]+type="file"[^>]*>', html)
for m in matches:
    print(m)
