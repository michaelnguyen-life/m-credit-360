# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''function mockModalLookup() {
        const mst = document.getElementById('modal-tax-id-input').value.trim();
        const nameInput = document.getElementById('modal-company-name-input');'''

replacement = '''function mockModalLookup() {
        const mst = document.getElementById('modal-tax-id').value.trim();
        const nameInput = document.getElementById('modal-company-name');'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    # Use regex
    pattern = r"const mst = document\.getElementById\('modal-tax-id-input'\)\.value\.trim\(\);\s*const nameInput = document\.getElementById\('modal-company-name-input'\);"
    rep2 = "const mst = document.getElementById('modal-tax-id').value.trim();\n        const nameInput = document.getElementById('modal-company-name');"
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, rep2, content, flags=re.DOTALL)
        codecs.open('templates/index.html', 'w', 'utf-8').write(content)
        print("SUCCESS REGEX")
    else:
        print("FAILED TO FIND CORRUPTED BLOCK")
