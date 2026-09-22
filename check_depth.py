import re

file_path = "templates/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    # This is a naive check but good enough for well-formatted HTML
    opens = len(re.findall(r'<div\b[^>]*>', line))
    closes = len(re.findall(r'</div>', line))
    depth += opens - closes
    if i > 780 and i < 795:
        print(f"{i+1:04d} | Depth: {depth:02d} | Opens: {opens} Closes: {closes} | {line.strip()[:50].encode("ascii", "ignore").decode("ascii")}")

print(f'Final depth: {depth}')
