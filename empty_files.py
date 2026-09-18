# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

# Replace Xem tất cả (6) with Xem tất cả (0)
content = re.sub(r'Xem tất cả \(6\)', 'Xem tất cả (0)', content)

# Remove the hardcoded file items
pattern = r'(<div id="file-ingested-list" class="space-y-1\.5 text-xs">).*?(</div>\s*<button onclick="openUploadDrawer\(\)")'
replacement = r'\1\n            \2'

if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED TO FIND FILE LIST")
