import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('<!-- Box 1: Company Profile -->')
end = html.find('<!-- Box 3: Cross-Sell Metrics -->', start)
print(html[end:end+1000].encode('utf-8'))
