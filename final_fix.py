import io
import re

with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enterprise -> SME
html = html.replace('Enterprise AI Banking Workspace', 'SME AI Banking Workspace')
html = html.replace('Doanh nghiệp (Enterprise)', 'Doanh nghiệp (EB)')

# 2. Thẩm định AI -> Agent Thẩm định
html = html.replace('Thẩm định AI', 'Agent Thẩm định', 1)

# 3. Update upload drawer text
html = html.replace('Khởi động AI Engine (MaaS)...', 'Khởi động GreenNode MaaS LLM (Qwen 3.6 Flash)...')
html = html.replace('AI Đọc hiểu & Bóc tách BCTC...', 'AI Đọc hiểu & Bóc tách BCTC (Zero-Regex)...')
html = html.replace('Quét rủi ro pháp lý & OSINT 360°...', 'Quét rủi ro pháp lý & OSINT 360° đa tầng...')

# 4. Redesign OSINT panel
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
              </div>
              
'''
    html = html[:osint_start] + new_osint + html[flags_start:]

# 5. Redesign Cross Sell panel
cross_start = html.find('<!-- Cross-Sell Alert Panel -->')
# Look for the exact end of the cross sell panel in the original file
end_cross = html.find('<!-- Box 1: Hồ sơ khách hàng -->', cross_start) 
# wait, Box 1 is in col-span-3! The cross sell panel is inside col-span-4.
# The original structure:
# <!-- Cross-Sell Alert Panel -->
# <div class="executive-card p-3.5 space-y-2"> ... </div>
# </div> <!-- end of eb-results-container -->
# </div> <!-- end of col-span-4 -->
# <div class="xl:col-span-3 space-y-3.5">
# <!-- Box 1: Hồ sơ khách hàng -->
# Let's find '</div>\n        </div>\n\n        <div class="xl:col-span-3 space-y-3.5">'
cross_end_marker = '</div>\n        </div>\n\n        <div class="xl:col-span-3 space-y-3.5">'
cross_end = html.find(cross_end_marker, cross_start)

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
            </div>\n'''
    html = html[:cross_start] + new_cross_sell + html[cross_end:]

# 6. Remove M-CREDIT AI Insight but keep Box 1
box2_start = html.find('<!-- Box 2: M-CREDIT AI Insight -->')
tab2_start = html.find('<!-- ==================== TAB 2: RETAIL BANKING (RB) ==================== -->')
if box2_start != -1 and tab2_start != -1:
    # We want to remove everything from Box 2 down to the closing divs of section-eb.
    # The end of section-eb is just before TAB 2.
    # We need to leave </div>\n      </div>\n\n before TAB 2.
    # Let's find the closing divs.
    end_of_section_eb = html.rfind('</div>\n      </div>\n\n      <!-- ==================== TAB 2', 0, tab2_start + 100)
    if end_of_section_eb != -1:
        # Wait, if we remove Box 2, we just close col-span-3!
        # Box 1 ends, then Box 2 starts.
        # So we just replace from box2_start to end_of_section_eb with nothing!
        html = html[:box2_start] + html[end_of_section_eb:]

# 7. Update layout from 5-4-3 to 5-7-3? No, 5-4-3 is 12 columns.
# The user wants "cột danh mục hồ sơ KH".
# If we keep 5-4-3, we have 3 columns!
# Let's just KEEP 5-4-3, it perfectly balances to 12.
# Wait, the user specifically complained that I REMOVED the "cột danh mục hồ sơ KH".
# If I just keep 5-4-3, it's restored!

# 8. Fix JS Logic
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

js_osint_start = html.find('// Mockup OSINT 360 values')
js_osint_end = html.find("const flagsList = document.getElementById('eb-flags-list');")
if js_osint_start != -1 and js_osint_end != -1:
    new_js_osint = '''// Mockup OSINT 360 values
        const taxId = document.getElementById('eb-tax-id').value;
        if (taxId.includes("0318999888")) {
          // Alpha Group
          document.getElementById('osint-tax').innerHTML = "Nợ 120Tr"; document.getElementById('osint-tax').className = "font-bold text-red-600 font-mono";
          document.getElementById('osint-bid-summary').innerHTML = "Đã trúng 3 gói"; document.getElementById('osint-bid-summary').className = "font-bold text-blue-600";
          document.getElementById('osint-bid-details').innerHTML = 
            <div class="flex justify-between items-center"><span class="truncate pr-2">• Cung cấp VLXD Sở GTVT</span><span class="font-mono font-bold text-slate-800">12,5 Tỷ</span></div>
            <div class="flex justify-between items-center"><span class="truncate pr-2">• Thi công Trạm Y tế Huyện</span><span class="font-mono font-bold text-slate-800">8,2 Tỷ</span></div>
            <div class="flex justify-between items-center"><span class="truncate pr-2">• Cải tạo Trường THPT</span><span class="font-mono font-bold text-slate-800">4,1 Tỷ</span></div>
          ;
        } else {
          document.getElementById('osint-tax').innerHTML = "Sạch (0đ)"; document.getElementById('osint-tax').className = "font-bold text-green-600 font-mono";
          document.getElementById('osint-bid-summary').innerHTML = "0 gói thầu"; document.getElementById('osint-bid-summary').className = "font-bold text-slate-500";
          document.getElementById('osint-bid-details').innerHTML = <div class="text-slate-400 italic">Chưa ghi nhận lịch sử trúng thầu</div>;
        }
        
        // Cross Sell Panel Population
        const crossList = document.getElementById('eb-cross-list');
        crossList.innerHTML = '';
        const deals = data.cross_sell_opportunities || [];
        let totalDeal = 0;
        
        document.getElementById('eb-cross-count').textContent = ${deals.length} Cơ hội chốt Deal;
        
        if (deals.length === 0) {
            crossList.innerHTML = <div class="p-2.5 rounded-lg bg-slate-50 text-slate-500 text-center border border-slate-200">Không tìm thấy cơ hội bán chéo.</div>;
        } else {
            deals.forEach(deal => {
              totalDeal += deal.estimated_deal_size || 0;
              const prioClass = deal.priority === 'P1' ? 'bg-[#ECFDF3] text-[#027A48] border-[#A6F4C5]' : 'bg-[#EFF4FF] text-[#1D4ED8] border-[#B2CCFF]';
              crossList.innerHTML += 
                <details class="group bg-white rounded-lg border border-slate-200 overflow-hidden mb-2 shadow-sm">
                  <summary class="flex items-center justify-between p-2.5 cursor-pointer bg-slate-50 hover:bg-slate-100 transition list-none">
                    <div class="flex items-center gap-2">
                      <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-slate-400 group-open:-rotate-180 transition-transform"></i>
                      <span class="font-bold text-[#0B1739]"></span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-[9px] px-1.5 py-0.5 rounded border font-bold uppercase "></span>
                      <span class="font-mono font-bold text-[#FF5A00]"> Tỷ</span>
                    </div>
                  </summary>
                  <div class="p-2.5 text-slate-600 bg-white border-t border-slate-100 leading-relaxed text-[11px]">
                    
                  </div>
                </details>
              ;
            });
        }
        document.getElementById('eb-cross-total').textContent = Quy mô:  Tỷ;

        '''
    html = html[:js_osint_start] + new_js_osint + html[js_osint_end:]

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
