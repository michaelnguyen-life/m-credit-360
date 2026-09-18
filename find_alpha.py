import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('BCTC_2025_Alpha_Group')
print(content[idx-300:idx+500].encode('ascii', 'ignore').decode('ascii'))
