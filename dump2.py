with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
with open('out2.txt', 'w', encoding='utf-8') as fw:
    for i, line in enumerate(lines):
        if 'QĐ.039' in line or 'QD.039' in line or 'Q.039' in line:
            fw.write('\n'.join(lines[i-2:i+15]) + '\n\n')
