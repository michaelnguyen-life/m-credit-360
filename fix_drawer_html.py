import io
import re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_list = '''<div id="upload-file-rows" class="space-y-1.5 max-h-48 overflow-y-auto">
            <div class="p-2.5 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between text-xs">
              <div class="flex items-center gap-2 truncate">
                <span class="w-5 h-5 rounded bg-red-100 text-red-600 font-bold text-[9px] flex items-center justify-center font-mono">PDF</span>
                <span class="font-medium text-[#0B1739] truncate">BCTC_2025_Alpha_Group.pdf</span>
              </div>
              <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-0.5"><i data-lucide="check" class="w-3 h-3"></i> Đã bóc tách</span>
            </div>
          </div>'''

new_list = '''<div id="upload-file-rows" class="space-y-1.5 max-h-48 overflow-y-auto">
            <!-- Files will be dynamically added here -->
          </div>'''

html = html.replace(old_list, new_list)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
