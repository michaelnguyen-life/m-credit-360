import codecs
content = codecs.open('server.py', 'r', 'utf-8').read()
content = content.replace('{"role": "user", "content": f"Văn bản trích xuất:\n{text}"}', '{"role": "user", "content": f"Văn bản trích xuất:\\n{text}"}')
content = content.replace('{"role": "user", "content": f"Văn bản trích xuất:\r\n{text}"}', '{"role": "user", "content": f"Văn bản trích xuất:\\n{text}"}')
codecs.open('server.py', 'w', 'utf-8').write(content)
