import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix layout: 
# Replace xl:col-span-4 (form) -> xl:col-span-5
# Replace xl:col-span-5 (results) -> xl:col-span-7
html = html.replace('xl:col-span-4', 'xl:col-span-5', 1)
html = html.replace('xl:col-span-5 space-y-3.5', 'xl:col-span-7 space-y-3.5', 1)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
