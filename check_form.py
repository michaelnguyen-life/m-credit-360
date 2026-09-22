import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
start = html.find('id="eb-form"')
end = html.find('</form>', start)
print(html[end-1000:end+100])
