import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for kw in ['section-rb', 'exportRBDocxMemo', 'btn-export-rb-docx', 'rb-customer-id']:
    print(kw, 'found:', kw in html)
