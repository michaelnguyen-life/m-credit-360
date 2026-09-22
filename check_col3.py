import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<div class="xl:col-span-3 space-y-3.5">')
end = html.find('<!-- ==================== TAB 2: RETAIL BANKING', start)
print(html[start:end].encode('utf-8'))
