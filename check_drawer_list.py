import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('Danh sách file đã chọn:')
end = html.find('</div>', html.find('BCTC_2025_Alpha_Group.pdf', start)) + 30
print(html[start:end].encode('utf-8'))
