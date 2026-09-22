import io
import re

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_clean = r"num_str = match.group(1).replace('.', '')"
new_clean = r"num_str = match.group(1).replace('.', '').replace(',', '')"

code = code.replace(old_clean, new_clean)

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
