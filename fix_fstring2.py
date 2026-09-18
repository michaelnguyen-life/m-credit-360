import codecs
import re

content = codecs.open('server.py', 'r', 'utf-8').read()
content = re.sub(r'\{"role": "user", "content": f"Văn bản trích xuất:\r?\n\{text\}"\}', '{"role": "user", "content": f"Văn bản trích xuất:\\\\n{text}"}', content)
codecs.open('server.py', 'w', 'utf-8').write(content)
