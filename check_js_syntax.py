import io
import esprima

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script>') + 8
end = html.rfind('</script>')
js_code = html[start:end]

try:
    esprima.parseScript(js_code)
    print("JS IS VALID")
except Exception as e:
    print("JS ERROR:", e)
