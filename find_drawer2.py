import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('id="upload-file-rows"')
end_idx = content.find('</div>', idx)
end_idx = content.find('</div>', end_idx + 1)
end_idx = content.find('</div>', end_idx + 1)
print(content[idx:end_idx+6].encode('ascii', 'ignore').decode('ascii'))
