import io
import re

with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Text Replacements
html = html.replace('Enterprise AI Banking Workspace', 'SME AI Banking Workspace')
html = html.replace('Doanh nghiệp (Enterprise)', 'Doanh nghiệp (EB)')
html = html.replace('Thẩm định AI', 'Agent Thẩm định', 1)
html = html.replace('Khởi động AI Engine (MaaS)...', 'Khởi động GreenNode MaaS LLM (Qwen 3.6 Flash)...')
html = html.replace('AI Đọc hiểu & Bóc tách BCTC...', 'AI Đọc hiểu & Bóc tách BCTC (Zero-Regex)...')
html = html.replace('Quét rủi ro pháp lý & OSINT 360°...', 'Quét rủi ro pháp lý & OSINT 360° đa tầng...')

# 2. Add Save Button
btn_area = '''        <!-- Right: Primary CTA Execution Buttons -->
        <div class="flex items-center space-x-2">
          <button onclick="runEBAssessment()" id="btn-run-eb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            <span>CHẠY THẨM ĐỊNH AI 360°</span>
          </button>
        </div>'''
new_btn_area = '''        <!-- Right: Primary CTA Execution Buttons -->
        <div class="flex items-center space-x-2">
          <button onclick="saveEBProfile()" id="btn-save-eb" class="px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="save" class="w-3.5 h-3.5"></i>
            <span>LƯU HỒ SƠ</span>
          </button>
          <button onclick="runEBAssessment()" id="btn-run-eb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            <span>CHẠY THẨM ĐỊNH AI 360°</span>
          </button>
        </div>'''
html = html.replace(btn_area, new_btn_area)

# 3. Add onblur to MST
mst_input = 'id="eb-tax-id" type="text" placeholder="Ví dụ: 0101234567"'
mst_input_new = 'id="eb-tax-id" type="text" placeholder="Ví dụ: 0101234567" onblur="loadEBProfile(this.value)"'
html = html.replace(mst_input, mst_input_new)

# 4. OSINT HTML
osint_start = html.find('<!-- OSINT Mini Dashboard -->')
flags_start = html.find('<!-- Financial Red Flags List -->')
if osint_start != -1 and flags_start != -1:
    new_osint = '''              <!-- OSINT Mini Dashboard -->
              <div class="space-y-2 text-[10px]">
                <div class="flex items-center justify-between p-2 bg-slate-50 rounded-lg border border-slate-200" title="Tra cứu Tổng cục Thuế">
                  <span class="text-slate-600 flex items-center gap-1.5 font-semibold"><i data-lucide="landmark" class="w-3.5 h-3.5 text-red-500"></i> Nợ thuế (GDT)</span>
                  <span id="osint-tax" class="font-bold text-red-600 font-mono">Đang quét...</span>
                </div>
                <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1.5" title="Hệ thống Mạng đấu thầu Quốc gia">
                    <span class="text-slate-600 flex items-center gap-1.5 font-semibold"><i data-lucide="award" class="w-3.5 h-3.5 text-blue-500"></i> Mua sắm công</span>
                    <span id="osint-bid-summary" class="font-bold text-blue-600">Đang quét...</span>
                  </div>
                  <div id="osint-bid-details" class="text-[10px] text-slate-600 pl-5 border-l-2 border-blue-100 space-y-1">
                  </div>
                </div>
              </div>\n'''
    html = html[:osint_start] + new_osint + html[flags_start:]

# 5. Cross-sell HTML
cross_start = html.find('<!-- Cross-Sell Alert Panel -->')
cross_end = html.find('<!-- COLUMN 3: RIGHT PANEL', cross_start)
if cross_start != -1 and cross_end != -1:
    new_cross_sell = '''            <!-- Cross-Sell Alert Panel -->
            <div class="executive-card p-3.5 space-y-2">
              <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2">
                <div class="flex flex-col">
                  <span class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5">
                    <i data-lucide="crosshair" class="w-4 h-4 text-[#FF5A00]"></i>
                    <span>Cơ hội Bán chéo (Cross-sell Alert)</span>
                  </span>
                  <span id="eb-cross-count" class="text-[10px] text-slate-500 mt-0.5 ml-5">Đang phân tích...</span>
                </div>
                <span id="eb-cross-total" class="text-[10px] px-2 py-0.5 rounded-full bg-[#ECFDF3] text-[#027A48] border border-[#A6F4C5] font-mono font-bold">
                  Quy mô: 0,0 Tỷ
                </span>
              </div>
              
              <div id="eb-cross-list" class="space-y-2 text-[11px] pt-1 max-h-48 overflow-y-auto pr-1">
                 <!-- JS populates this -->
              </div>
            </div>

          </div>
        </div>

        '''
    html = html[:cross_start] + new_cross_sell + html[cross_end:]

# 6. Remove M-CREDIT AI Insight (Box 2)
box2_start = html.find('<!-- Box 2: M-CREDIT AI Insight -->')
if box2_start != -1:
    end_of_box2 = html.find('</div>\\n      </div>\\n\\n      <!-- ==================== TAB 2', box2_start)
    if end_of_box2 != -1:
        html = html[:box2_start] + html[end_of_box2:]

# 7. JS fixes in runEBAssessment
js_start = html.find('// Set OSINT loading state')
js_end = html.find('lucide.createIcons();', js_start)
if js_start != -1 and js_end != -1:
    new_js = '''// Set OSINT loading state
      ['osint-tax', 'osint-bid-summary'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.innerHTML = '<span class="flex items-center gap-1"><i data-lucide="loader-2" class="w-3 h-3 animate-spin"></i> Tra cứu...</span>';
          el.className = "text-slate-400 font-medium";
        }
      });
      const bidDetails = document.getElementById('osint-bid-details');
      if (bidDetails) bidDetails.innerHTML = '';
      '''
    html = html[:js_start] + new_js + html[js_end:]

# NEW 7.5 Fix: The OSINT mockup JS in temp_backup.html is slightly different!
# Let's just find // Mockup OSINT and lucide.createIcons(); after it!
osint_code_start = html.find('// Mockup OSINT')
# In temp_backup.html, after OSINT mockup, there is NO eb-flags-list logic.
# Wait, let's see what is after // Mockup OSINT.
# I will just replace from // Mockup OSINT to lucide.createIcons();!
