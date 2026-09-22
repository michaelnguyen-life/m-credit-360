import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('rb-gross-income')
print('Found at:', idx)
print(html[max(0, idx-1000):min(len(html), idx+1000)])
