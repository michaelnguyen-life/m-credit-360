with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'switchTab' in line:
        with open('test_out.txt', 'w', encoding='utf-8') as fw:
            fw.write('\n'.join(lines[i-15:i+15]))
        break
