import codecs

lines = codecs.open('server.py', 'r', 'utf-8').readlines()
for i, line in enumerate(lines):
    if 'Van b?n' in line or 'Văn bản' in line or 'role' in line and 'user' in line and 'content' in line and 'f"' in line:
        if '{text' not in line:
            # It's split across lines!
            lines[i] = '                    {"role": "user", "content": f"Văn bản trích xuất:\\n{text[:6000]}"}\n'
            lines[i+1] = '' # clear the next line which has the closing brace
            
codecs.open('server.py', 'w', 'utf-8').writelines(lines)
