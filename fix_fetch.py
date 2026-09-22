import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken fetch!
broken_fetch = 'await fetch(/api/load-eb/);'
fixed_fetch = 'await fetch(/api/load-eb/);'
if broken_fetch in html:
    html = html.replace(broken_fetch, fixed_fetch)
else:
    print('Not found exact broken string')

# Wait, let's just use regex
import re
html = re.sub(r'fetch\(/api/load-eb/\);', 'fetch(/api/load-eb/);', html)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
