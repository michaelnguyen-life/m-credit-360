# -*- coding: utf-8 -*-
import codecs
content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''        document.getElementById('eb-principal').value = princ.toLocaleString('vi-VN');'''
replacement = '''        document.getElementById('eb-principal').value = princ.toLocaleString('vi-VN');
        window.pendingEBData = d;'''

new_content = content.replace(target, replacement)
codecs.open('templates/index.html', 'w', 'utf-8').write(new_content)
