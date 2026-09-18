# -*- coding: utf-8 -*-
import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''      // Show Intelligent Empty State, Hide Results
      document.getElementById('eb-results-container').classList.add('hidden');
      document.getElementById('eb-empty-state').classList.remove('hidden');
      lucide.createIcons();
    }'''

replacement = '''      // Show Intelligent Empty State, Hide Results
      document.getElementById('eb-results-container').classList.add('hidden');
      document.getElementById('eb-empty-state').classList.remove('hidden');
      
      // Clear File List in Sidebar
      const fileList = document.getElementById('file-ingested-list');
      if (fileList) fileList.innerHTML = '';
      const allFilesLink = document.querySelector('a[href="#all-files"]');
      if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (0)';

      lucide.createIcons();
    }'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED TO FIND TARGET")
