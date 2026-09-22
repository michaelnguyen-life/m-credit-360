import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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
html = html.replace(box2_html, '')
html = html.replace('\n\n\n', '\n') # clean up newlines

# Where to inject it?
# Let's find:
target_text = '''                <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-0.5 flex-shrink-0"><i data-lucide="check" class="w-3 h-3"></i> Đã bóc tách</span>
              </div>
            </div>
          </div>'''

if target_text in html:
    html = html.replace(target_text, target_text + '\n' + box2_html)
else:
    print("Could not find target_text!")

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
