# -*- coding: utf-8 -*-
import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''      // Clear File List in Sidebar
      const fileList = document.getElementById('file-ingested-list');
      if (fileList) fileList.innerHTML = '';
      const allFilesLink = document.querySelector('a[href="#all-files"]');
      if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (0)';

      lucide.createIcons();
    }'''

replacement = '''      // Clear File List in Sidebar
      const fileList = document.getElementById('file-ingested-list');
      if (fileList) fileList.innerHTML = '';
      const allFilesLink = document.querySelector('a[href="#all-files"]');
      if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (0)';
      
      // Clear AI Insight in Sidebar
      const insightText = document.getElementById('ai-insight-text');
      if (insightText) insightText.textContent = 'Chưa có dữ liệu đánh giá. Vui lòng chạy phân tích AI.';

      lucide.createIcons();
    }'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED TO FIND TARGET")
