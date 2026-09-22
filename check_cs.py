import io
with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('<!-- Cross-Sell Alert Panel -->')
end = html.find('<!-- Box 1: Hồ sơ khách hàng -->', start)
if end != -1:
    end = html.rfind('<div class="xl:col-span-3 space-y-3.5">', start, end)
print(html[start:end].encode('utf-8'))
