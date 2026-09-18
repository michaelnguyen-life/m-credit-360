# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

pattern = r'(<div id="upload-file-rows" class="space-y-1\.5 max-h-48 overflow-y-auto">).*?(</div>\s*</div>\s*</div>\s*<!-- Drawer Footer -->)'
replacement = r'\1\n          \2'

if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    print("SUCCESS 1")

# Also add clearing to confirmNewCustomerSession
target = '''      // Clear AI Insight in Sidebar
      const insightText = document.getElementById('ai-insight-text');
      if (insightText) insightText.textContent = 'Chưa có dữ liệu đánh giá. Vui lòng chạy phân tích AI.';'''

replacement2 = '''      // Clear AI Insight in Sidebar
      const insightText = document.getElementById('ai-insight-text');
      if (insightText) insightText.textContent = 'Chưa có dữ liệu đánh giá. Vui lòng chạy phân tích AI.';
      
      // Clear Upload Drawer Files
      const uploadRows = document.getElementById('upload-file-rows');
      if (uploadRows) uploadRows.innerHTML = '';'''

if target in content:
    content = content.replace(target, replacement2)
    print("SUCCESS 2")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
