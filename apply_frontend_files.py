import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

alpha_files_js = '''
              if (type === 'alpha') {
                  document.getElementById('eb-docs-list').innerHTML = `
                    <div class="p-2 rounded-lg bg-slate-50 border flex items-center justify-between">
                      <div class="flex items-center gap-2 truncate">
                        <span class="w-5 h-5 rounded bg-red-100 text-red-600 font-bold text-[9px] flex items-center justify-center font-mono">PDF</span>
                        <div class="truncate">
                          <span class="font-semibold text-[#0B1739] block truncate text-[11px]">BCTC_2025_Alpha_Group.pdf</span>
                          <span class="text-[9px] text-[#98A2B3]">PDF • 4.2 MB</span>
                        </div>
                      </div>
                      <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-0.5 flex-shrink-0"><i data-lucide="check" class="w-3 h-3"></i> Đã bóc tách</span>
                    </div>
                  `;
              } else if (type === 'beta') {
                  document.getElementById('eb-docs-list').innerHTML = `
                    <div class="p-2 rounded-lg bg-slate-50 border flex items-center justify-between">
                      <div class="flex items-center gap-2 truncate">
                        <span class="w-5 h-5 rounded bg-red-100 text-red-600 font-bold text-[9px] flex items-center justify-center font-mono">PDF</span>
                        <div class="truncate">
                          <span class="font-semibold text-[#0B1739] block truncate text-[11px]">BCTC_Beta_Corp_2024.pdf</span>
                          <span class="text-[9px] text-[#98A2B3]">PDF • 3.5 MB</span>
                        </div>
                      </div>
                      <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-0.5 flex-shrink-0"><i data-lucide="check" class="w-3 h-3"></i> Đã bóc tách</span>
                    </div>
                  `;
              }
              lucide.createIcons();
'''

target = "const d = await res.json();"
if "if (type === 'alpha')" not in html:
    html = html.replace(target, target + '\n' + alpha_files_js)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
