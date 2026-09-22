import io
with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('KẾT QUẢ THẨM ĐỊNH SƠ BỘ MSB')
end = html.find('Cơ hội Bán chéo', start)
print(html[start:end].encode('utf-8'))
