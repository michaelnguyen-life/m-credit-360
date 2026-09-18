import codecs
import re
content = codecs.open('templates/index.html', 'r', 'utf-8').read()

pattern = r'<div id="file-ingested-list"[^>]*>.*?</div>\s*</div>\s*<!-- M-CREDIT AI Insight -->'
if re.search(pattern, content, flags=re.DOTALL):
    print("FOUND")
else:
    print("NOT FOUND")
