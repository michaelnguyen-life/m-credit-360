import re
with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

def json_replacer(match):
    text = match.group(0)
    text = text.replace('True', 'true')
    text = text.replace('False', 'false')
    return text

content = re.sub(r"json\.loads\('''\{.*?\}'''\)", json_replacer, content, flags=re.DOTALL)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
