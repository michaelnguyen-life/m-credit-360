import io, re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract script tag content
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f"Total script blocks: {len(scripts)}")
if scripts:
    with io.open('extracted_script.js', 'w', encoding='utf-8') as sf:
        sf.write(scripts[0])
    print("Wrote extracted_script.js (size: {})".format(len(scripts[0])))

# Find all onclick handlers
onclicks = re.findall(r'onclick=["\'](.*?)["\']', html)
print(f"Total onclick handlers: {len(onclicks)}")
unique_onclicks = sorted(list(set(onclicks)))
for oc in unique_onclicks:
    print("  -", oc)
