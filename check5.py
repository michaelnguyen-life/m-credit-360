import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find end of section-eb
eb_start = html.find('id="section-eb"')
eb_end = html.find('</div>\n          </div>\n        </div>', eb_start)
print(html[eb_end:eb_end+1500].encode('utf-8'))
