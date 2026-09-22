import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

def get_depth(text):
    opens = len(re.findall(r'<div\b[^>]*>', text))
    closes = len(re.findall(r'</div>', text))
    return opens - closes

depth = 0
for i, line in enumerate(lines):
    if "id=\"section-rb\"" in line:
        target_rb_line = i
        break
    depth += get_depth(line)

print(f"Depth before section-rb: {depth}")

depth = 0
for i, line in enumerate(lines):
    if "<footer" in line:
        target_footer_line = i
        break
    depth += get_depth(line)

print(f"Depth before footer: {depth}")

print(f'Final depth: {depth + sum(get_depth(line) for line in lines[target_footer_line:])}')
