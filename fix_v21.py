import codecs

content = codecs.open('server.py', 'r', 'utf-8').read()

target = '''                def safe_int(val, default):
                    try:
                        v = int(val)
                        return v if v != 0 else default
                    except:
                        return default'''

replacement = '''                def safe_int(val, default):
                    if val is None or str(val).strip() == "": return 0
                    try:
                        clean_str = str(val).replace(".", "").replace(",", "").replace(" ", "")
                        v = int(clean_str)
                        return v
                    except:
                        return 0'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('server.py', 'w', 'utf-8').write(content)
    print("SUCCESS server.py")
else:
    print("FAILED server.py")

content_html = codecs.open('templates/index.html', 'r', 'utf-8').read()
target_html = '''fileList.innerHTML = fileHTML; // Replace list with this single file for simplicity, or append.'''
replacement_html = '''fileList.insertAdjacentHTML('beforeend', fileHTML);'''

if target_html in content_html:
    content_html = content_html.replace(target_html, replacement_html)
    
    # Also update the file count
    # const allFilesLink = document.querySelector('a[href="#all-files"]');
    # if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (1)';
    # We should dynamically update the count based on fileList.children.length
    count_target = '''                  const allFilesLink = document.querySelector('a[href="#all-files"]');
                  if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (1)';'''
    count_replace = '''                  const allFilesLink = document.querySelector('a[href="#all-files"]');
                  if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (' + fileList.children.length + ')';'''
    content_html = content_html.replace(count_target, count_replace)
    
    codecs.open('templates/index.html', 'w', 'utf-8').write(content_html)
    print("SUCCESS index.html")
else:
    print("FAILED index.html")
