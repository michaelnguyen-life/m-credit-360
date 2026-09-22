import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<!-- Box 2: M-CREDIT AI Insight -->')
end = html.find('        </div>\n      </div>\n\n      <!-- ==================== TAB 2: RETAIL BANKING', start)

# Let's verify what we are deleting:
print(html[start:end].encode('utf-8'))
