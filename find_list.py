import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('file-ingested-list')
print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
