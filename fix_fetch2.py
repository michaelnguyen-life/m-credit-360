import io
import re
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'fetch\(/api/load-eb/\);', 'fetch(`/api/load-eb/${mst}`);', html)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
