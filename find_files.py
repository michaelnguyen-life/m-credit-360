import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('id="file-ingested-list"')
print(content[idx:idx+2500].encode('ascii', 'ignore').decode('ascii'))
