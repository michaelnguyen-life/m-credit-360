import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('id="file-ingested-list"')
print(content[idx+2500:idx+4500].encode('ascii', 'ignore').decode('ascii'))
