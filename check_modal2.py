import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<!-- Extracted Fields Table -->')
end = html.find('</div>', html.find('Áp dụng dữ liệu từ hồ sơ', start)) + 15
print(html[start:end].encode('utf-8'))
