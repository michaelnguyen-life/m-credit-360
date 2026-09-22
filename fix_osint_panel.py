import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's insert OSINT Mini Dashboard right before the Red Flags Panel in the middle column
red_flags_panel = '            <!-- Red Flags Panel -->'

osint_html = '''
            <!-- OSINT Mini Dashboard -->
            <div class="executive-card p-3.5 space-y-2">
              <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2">
                <span class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5">
                  <i data-lucide="globe" class="w-4 h-4 text-[#3B82F6]"></i>
                  <span>Trinh sát Dữ liệu (OSINT 360°)</span>
                </span>
              </div>
              <div class="space-y-2 text-[11px] pt-1">
                <div class="flex items-center justify-between p-2 bg-slate-50 rounded-lg border border-slate-200">
                  <span class="text-slate-600 flex items-center gap-1.5 font-semibold"><i data-lucide="landmark" class="w-3.5 h-3.5 text-red-500"></i> Nợ thuế (Tổng cục Thuế)</span>
                  <span id="osint-tax" class="font-bold text-slate-400 font-mono">Chưa quét</span>
                </div>
                <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-slate-600 flex items-center gap-1.5 font-semibold"><i data-lucide="award" class="w-3.5 h-3.5 text-blue-500"></i> Mua sắm công</span>
                    <span id="osint-bid-summary" class="font-bold text-slate-400">Chưa quét</span>
                  </div>
                  <div id="osint-bid-details" class="text-[10px] text-slate-600 pl-5 border-l-2 border-blue-100 space-y-1">
                  </div>
                </div>
              </div>
            </div>
'''

if '<!-- OSINT Mini Dashboard -->' not in html:
    html = html.replace(red_flags_panel, osint_html + '\n' + red_flags_panel)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
