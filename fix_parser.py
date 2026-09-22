import io
import re

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_func = '''    financials = {}
    lines = text.lower().split('\\n')'''

new_func = '''    financials = {}
    # Fix weird pdf control characters
    for ch in range(1, 32):
        if ch != 10: # keep newline
            text = text.replace(chr(ch), ' ')
    lines = text.lower().split('\\n')'''

code = code.replace(old_func, new_func)

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
