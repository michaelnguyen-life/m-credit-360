import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<!-- Box 2: M-CREDIT AI Insight -->')
end = html.find('        </div>\n      </div>\n\n      <!-- ==================== TAB 2: RETAIL BANKING', start)

if start != -1 and end != -1:
    html = html[:start] + html[end:]

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
