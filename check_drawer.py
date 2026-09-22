import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="upload-drawer"')
end = html.find('</div>', html.find('file-input', start)) + 50
print(html[start:end])
