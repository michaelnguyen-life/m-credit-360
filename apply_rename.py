import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('Xuất tờ trình MB02a (.docx)', 'Xuất tờ trình')

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
