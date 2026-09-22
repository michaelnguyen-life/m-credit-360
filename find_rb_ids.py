import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [(m.start(), m.group()) for m in re.finditer(r'id=["\'][^"\']*rb[^"\']*["\']', html, re.IGNORECASE)]
print('Matches with rb in id:', len(matches))
for pos, s in matches:
    print(pos, ':', s)
