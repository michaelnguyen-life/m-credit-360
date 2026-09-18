import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

# 1. Add 'multiple' to file input
content = content.replace('<input id="file-upload" type="file" class="hidden" onchange="handleFileSelect(event)" accept=".pdf,.xlsx,.xls,.doc,.docx,.jpg,.png" />', 
                          '<input id="file-upload" type="file" class="hidden" onchange="handleFileSelect(event)" accept=".pdf,.xlsx,.xls,.doc,.docx,.jpg,.png" multiple />')

# 2. Rewrite handleFileSelect
target_func = '''function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      const file = files[0];
      currentUploadedFileName = file.name || "BCTC_Uploaded.pdf";'''

replacement_func = '''function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      
      const fileList = document.getElementById('file-ingested-list');
      
      // 1. Add all files to the sidebar immediately
      for (let i = 0; i < files.length; i++) {
          const f = files[i];
          const fileId = "file-" + Date.now() + "-" + i;
          const fileHTML = <div id="\" class="flex items-center justify-between p-2 rounded bg-white border border-[#EAECF0] hover:border-[#FF5A00] transition">
                        <div class="flex items-center gap-2 overflow-hidden">
                            <i data-lucide="file-text" class="w-4 h-4 text-[#FF5A00] shrink-0"></i>
                            <span class="text-xs text-[#344054] truncate" title="\">\</span>
                        </div>
                        <button onclick="deleteUploadedFile('\')" class="text-gray-400 hover:text-red-500 transition" title="Xóa tài liệu">
                            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                        </button>
                      </div>;
          if (fileList) fileList.insertAdjacentHTML('beforeend', fileHTML);
      }
      
      // Update count
      if (fileList) {
          const allFilesLink = document.querySelector('a[href="#all-files"]');
          if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (' + fileList.children.length + ')';
      }
      if (typeof lucide !== 'undefined') lucide.createIcons();

      // 2. Pick the best file for AI Extraction (prefer BCTC)
      let targetFile = files[0];
      for (let i = 0; i < files.length; i++) {
          if (files[i].name.toLowerCase().includes('bctc')) {
              targetFile = files[i];
              break;
          }
      }
      
      const file = targetFile;
      currentUploadedFileName = file.name || "BCTC_Uploaded.pdf";'''

if target_func in content:
    content = content.replace(target_func, replacement_func)
else:
    print("FAILED TO REPLACE FUNC")

# 3. We also need to remove the sidebar adding logic from the fetch SUCCESS block because we already added it!
# Wait, I'll just use regex to remove the fileList logic in the success block.
import re
# Find the success block fileList logic
success_file_list_regex = r'''\s*// Add file to sidebar list.*?if\s*\(typeof lucide !== 'undefined'\) lucide\.createIcons\(\);\s*\}\s*// AUTOMATICALLY RUN ASSESSMENT'''

if re.search(success_file_list_regex, content, flags=re.DOTALL):
    content = re.sub(success_file_list_regex, '\n                  // AUTOMATICALLY RUN ASSESSMENT', content, flags=re.DOTALL)
else:
    print("FAILED TO REMOVE OLD LIST LOGIC")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
print("SUCCESS")
