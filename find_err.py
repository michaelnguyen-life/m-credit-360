with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
m = re.findall(r'<script[^>]*>([\s\S]*?)<\/script>', content, re.IGNORECASE)
script = m[1]
lines = script.split('\n')
for i, line in enumerate(lines):
    try:
        compile(line, 'script', 'exec')
    except SyntaxError as e:
        if '<' in line:
            print(f"Line {i+1}: {line}")
