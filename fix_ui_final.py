import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''const fileHTML =                       <div id="" class="flex items-center justify-between p-2 rounded bg-white border border-[#EAECF0] hover:border-[#FF5A00] transition">
                        <div class="flex items-center gap-2 overflow-hidden">
                            <i data-lucide="file-text" class="w-4 h-4 text-[#FF5A00] shrink-0"></i>
                            <span class="text-xs text-[#344054] truncate" title="">\</span>
                        </div>
                        <button onclick="deleteUploadedFile('')" class="text-gray-400 hover:text-red-500 transition" title="Xóa tài liệu">
                            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                        </button>
                      </div>\\;'''

replacement = '''const fileHTML = \
                      <div id="\" class="flex items-center justify-between p-2 rounded bg-white border border-[#EAECF0] hover:border-[#FF5A00] transition">
                        <div class="flex items-center gap-2 overflow-hidden">
                            <i data-lucide="file-text" class="w-4 h-4 text-[#FF5A00] shrink-0"></i>
                            <span class="text-xs text-[#344054] truncate" title="\">\</span>
                        </div>
                        <button onclick="deleteUploadedFile('\')" class="text-gray-400 hover:text-red-500 transition" title="Xóa tài liệu">
                            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                        </button>
                      </div>\;'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
