import io
with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<div class="xl:col-span-3 space-y-3.5">')
if start != -1:
    print(html[start:start+1000].encode('utf-8'))
