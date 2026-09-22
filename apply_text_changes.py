import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace targets
html = html.replace('KẾT QUẢ THẨM ĐỊNH SƠ BỘ MSB', 'KẾT QUẢ THẨM ĐỊNH SƠ BỘ')
html = html.replace('Trinh sát Dữ liệu (OSINT 360°)', 'Trinh sát Dữ liệu công khai')

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
