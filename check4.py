import io
with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<div class="xl:col-span-3 space-y-3.5">')
if start != -1:
    end = html.find('<!-- ==================== TAB 2: RETAIL BANKING (RB) ==================== -->')
    print(html[start:end].encode('utf-8'))
