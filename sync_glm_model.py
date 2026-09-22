import io

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Make GREENNODE_MODEL configurable from ENV and default to GLM 5.2 Hackathon
old_model = 'GREENNODE_MODEL = "qwen/qwen3.6-flash"'
new_model = 'GREENNODE_MODEL = os.environ.get("GREENNODE_MODEL", "z-ai/glm-5.2-hackathon")'

if old_model in code:
    code = code.replace(old_model, new_model)
    with io.open('server.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated server.py model config!")
else:
    print("Pattern not found in server.py")

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_badge = 'GreenNode MaaS • qwen/qwen3.6-flash'
new_badge = 'GreenNode MaaS • z-ai/glm-5.2-hackathon'

if old_badge in html:
    html = html.replace(old_badge, new_badge)
    with io.open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html badge to GLM 5.2 Hackathon!")
else:
    print("Badge not found in index.html")
