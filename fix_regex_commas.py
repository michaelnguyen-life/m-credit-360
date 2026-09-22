import io
import re

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_regex = r"match = re.search(pattern + r'.*?(\d{1,3}(?:\.\d{3})+)', text)"
new_regex = r"match = re.search(pattern + r'.*?(\d{1,3}(?:[.,]\d{3})+)', text)"

code = code.replace(old_regex, new_regex)

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
