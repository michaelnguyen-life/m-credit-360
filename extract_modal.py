import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()
idx = content.find('new-customer-modal')
codecs.open('modal.txt', 'w', 'utf-8').write(content[max(0, idx-100):idx+2500])
