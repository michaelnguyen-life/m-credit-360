import codecs

content = codecs.open('server.py', 'r', 'utf-8').read()

target = '''                from pypdf import PdfReader
                text = "
".join(page.extract_text() or "" for page in PdfReader(str(tmp_path)).pages)
            except Exception as e:'''

replacement = '''                from pypdf import PdfReader
                text = "\\n".join(page.extract_text() or "" for page in PdfReader(str(tmp_path)).pages)
            except Exception as e:'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('server.py', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
