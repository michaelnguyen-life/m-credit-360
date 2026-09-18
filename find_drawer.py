import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('BCTC_2025_Alpha_Group')
start = content.rfind('<div', 0, idx)
start = content.rfind('<div', 0, start)
start = content.rfind('<div', 0, start)
print(content[start:idx+1500].encode('ascii', 'ignore').decode('ascii'))
