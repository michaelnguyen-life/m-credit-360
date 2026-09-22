import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("document.getElementById('eb-docs-list')", "document.getElementById('file-ingested-list')")

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
