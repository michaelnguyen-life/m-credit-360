import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('fetch(\'/api/upload\'')
print(content[idx+1000:idx+2500].encode('ascii', 'ignore').decode('ascii'))
