import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

script_matches = re.finditer(r'<script[^>]*>([\s\S]*?)<\/script>', content, re.IGNORECASE)
for i, m in enumerate(script_matches):
    script_content = m.group(1).strip()
    if script_content:
        if 'switchTab' in script_content:
            with open(f'script_{i+1}_out.txt', 'w', encoding='utf-8') as fw:
                fw.write(script_content)
        else:
            with open(f'script_{i+1}_out.txt', 'w', encoding='utf-8') as fw:
                fw.write(script_content[:200] + "\n... (truncated)")
