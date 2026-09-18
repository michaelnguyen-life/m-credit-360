import codecs
from bs4 import BeautifulSoup
soup = BeautifulSoup(codecs.open('templates/index.html', 'r', 'utf-8').read(), 'html.parser')
js = '\n'.join([s.string for s in soup.find_all('script') if s.string])
codecs.open('test5.js', 'w', 'utf-8').write(js)
