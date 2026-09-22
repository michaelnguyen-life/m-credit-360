import io
import re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First, remove the previously injected Box 2 if it's there
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

# Now find file-ingested-list
match = re.search(r'<div id="file-ingested-list" class="space-y-1.5 text-xs">.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
if match:
    # We want to replace the inside of file-ingested-list with empty
    # Wait, the regex `.*?</div>` will stop at the first `</div>`
    # Let's just find `<!-- Box 1: Hồ sơ khách hàng -->`
    box1_start = html.find('<!-- Box 1: Hồ sơ khách hàng -->')
    box1_end = html.find('</div>\n        </div>', box1_start) # This is the end of the xl:col-span-3! Wait no.
    # Let's do it cleanly by searching for the start and finding the matching closing tag.
    pass

# Clean way:
target_box1_end = '''              </div>
            </div>
          </div>'''

# wait, we can just find 'id="file-ingested-list"'
# and replace everything inside it up to the end of the card.
# The card ends before '</div>\n        </div>\n      </div>\n    </div>\n  </main>'

print("Applying regex replacement...")
html = re.sub(
    r'<div id="file-ingested-list" class="space-y-1\.5 text-xs">.*?(?=\n          </div>\n        </div>)',
    r'<div id="file-ingested-list" class="space-y-1.5 text-xs">\n              <!-- Files will be injected here -->\n            </div>',
    html,
    flags=re.DOTALL
)

# Now inject Box 2 right after Box 1 (which ends with `</div>\n          </div>`)
# Let's find:
box1_full = '''<div id="file-ingested-list" class="space-y-1.5 text-xs">
              <!-- Files will be injected here -->
            </div>
          </div>'''
if box1_full in html:
    html = html.replace(box1_full, box1_full + '\n' + box2_html)
else:
    print("Could not find box1_full")

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
