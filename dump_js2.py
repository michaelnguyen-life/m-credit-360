import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.rfind('<script>') + 8
end = html.rfind('</script>')
js_code = html[start:end]

with io.open('test.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
