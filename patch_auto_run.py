import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''                  const allFilesLink = document.querySelector('a[href="#all-files"]');
                  if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (1)';'''

replacement = '''                  const allFilesLink = document.querySelector('a[href="#all-files"]');
                  if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (1)';
                  
                  // AUTOMATICALLY RUN ASSESSMENT
                  setTimeout(() => {
                      if (typeof runEBAssessment === 'function') {
                          runEBAssessment();
                      }
                  }, 500);'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
