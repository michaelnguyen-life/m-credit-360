import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('function applyExtractedData() {')
end = html.find('document.getElementById(\'eb-empty-state\').classList.add(\'hidden\');', start)
print(html[start:end].encode('utf-8'))
