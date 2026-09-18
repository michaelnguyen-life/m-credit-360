with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
with open('out3.txt', 'w', encoding='utf-8') as fw:
    for i, line in enumerate(lines):
        if 'Phải thu' in line or 'Nhập khẩu' in line or 'Phi thu' in line or 'NhA' in line:
            fw.write('\n'.join(lines[i-2:i+5]) + '\n\n')
