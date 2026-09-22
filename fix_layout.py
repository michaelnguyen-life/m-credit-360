import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The injection started at index 18!
# Let's find the exact string that was injected.
box2_html = '''
          <!-- Box 2: M-CREDIT AI Insight -->
          <div id="ai-insight-box" class="executive-card p-3.5 space-y-2.5 hidden">
            <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2">
              <span class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5">
                <i data-lucide="sparkles" class="w-4 h-4 text-[#FF5A00]"></i>
                <span>M-CREDIT AI Insight</span>
              </span>
              <span class="text-[9px] px-1.5 py-0.5 rounded bg-orange-100 text-[#FF5A00] font-bold">Mới</span>
            </div>

            <div id="ai-insight-content" class="space-y-3 pt-1">
              <!-- AI insights will be injected here -->
            </div>

            <!-- Copilot Action Buttons -->
            <div class="grid grid-cols-2 gap-1.5 pt-2 border-t border-[#E6EAF0]">
              <button onclick="triggerAICopilot('Giải thích chi tiết các chỉ số tài chính yếu kém')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Giải thích
              </button>
              <button onclick="triggerAICopilot('Chạy kịch bản Stress Test dòng tiền nếu doanh thu giảm 15%')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Stress Test
              </button>
              <button onclick="exportDocxMemo()" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Soạn tờ trình
              </button>
              <button onclick="triggerAICopilot('Phân tích sâu rủi ro đòn bẩy và kiểm soát dòng tiền Rule 5D')" class="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-[#0B1739] font-medium text-[10px] transition text-center">
                Phân tích sâu
              </button>
            </div>
          </div>
'''
# Replace the FIRST occurrence of box2_html with empty string
html = html.replace(box2_html, '', 1)

# Now, we need to inject it in the correct place.
# We want it below Box 1.
# Box 1 ends with:
# <div id="eb-docs-list" class="space-y-2 text-xs">
#   ... (this was made empty or has alpha_files_js)
# </div>
# </div> <!-- End of Box 1 -->
# Let's find eb-docs-list
docs_list_idx = html.find('id="eb-docs-list"')
# Find the closing div of eb-docs-list
close_div_1 = html.find('</div>', docs_list_idx)
# Find the closing div of Box 1
close_div_2 = html.find('</div>', close_div_1 + 6) + 6

# Let's print out what we are about to inject after to be safe
print("Injecting after:")
print(html[close_div_2-50:close_div_2].encode('utf-8'))

html = html[:close_div_2] + '\n' + box2_html + html[close_div_2:]

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
