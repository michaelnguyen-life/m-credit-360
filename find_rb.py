import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = 'section-rb'
idx = html.find(target)
while idx != -1:
    print('--- Match at:', idx)
    print(html[idx-50:idx+250])
    idx = html.find(target, idx + 1)
