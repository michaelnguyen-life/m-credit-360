with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(': false,', ': False,')
content = content.replace(': true,', ': True,')

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
