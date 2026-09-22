import io

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
js_insert_point = html.find('lucide.createIcons();\\n      } catch (err) {')
if js_insert_point != -1:
    new_osint_js = '''
        // Dynamic OSINT & Cross-sell
        const osintData = data.osint || {
          tax_status: "Sạch (0đ)", tax_class: "text-green-600",
          bid_summary: "0 gói thầu", bid_class: "text-slate-500",
          bid_details: <div class="text-slate-400 italic">Chưa ghi nhận lịch sử trúng thầu</div>
        };
        
        document.getElementById('osint-tax').innerHTML = osintData.tax_status; 
        document.getElementById('osint-tax').className = ont-bold  font-mono;
        document.getElementById('osint-bid-summary').innerHTML = osintData.bid_summary; 
        document.getElementById('osint-bid-summary').className = ont-bold ;
        document.getElementById('osint-bid-details').innerHTML = osintData.bid_details;

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
        document.getElementById('eb-cross-total').textContent = Quy mô:  Tỷ;\n\n        '''
    html = html[:js_insert_point] + new_osint_js + html[js_insert_point:]

# 8. Add saveEBProfile and loadEBProfile at end of script
save_load_js = '''
    async function saveEBProfile() {
      const btn = document.getElementById('btn-save-eb');
      const origText = btn.innerHTML;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> LƯU...';
      
      const payload = {
        company: {
          name: document.getElementById('eb-company-name').value,
          tax_id: document.getElementById('eb-tax-id').value
        },
        reporting_period: document.getElementById('eb-period').value,
        financials: {
          BS001: parseVND(document.getElementById('eb-ca').value),
          BS002: parseVND(document.getElementById('eb-cl').value),
          BS003: parseVND(document.getElementById('eb-ar').value),
          BS004: parseVND(document.getElementById('eb-inv').value),
          BS005: parseVND(document.getElementById('eb-ap').value),
          BS006: parseVND(document.getElementById('eb-std').value),
          BS007: parseVND(document.getElementById('eb-tl').value),
          BS008: parseVND(document.getElementById('eb-equity').value),
          IS001: parseVND(document.getElementById('eb-revenue').value),
          IS002: parseVND(document.getElementById('eb-gp').value),
          IS003: parseVND(document.getElementById('eb-ebit').value),
          IS004: parseVND(document.getElementById('eb-interest').value),
          IS005: parseVND(document.getElementById('eb-np').value),
          CF001: parseVND(document.getElementById('eb-ocf').value),
          CF002: parseVND(document.getElementById('eb-icf').value),
          CF003: parseVND(document.getElementById('eb-fcf').value)
        }
      };
      
      try {
        const response = await fetch('/api/save-eb', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (response.ok) {
          btn.innerHTML = '<i data-lucide="check" class="w-3.5 h-3.5"></i> ĐÃ LƯU';
          setTimeout(() => { btn.innerHTML = origText; lucide.createIcons(); }, 2000);
        }
      } catch (err) {
        console.error(err);
        btn.innerHTML = origText;
        lucide.createIcons();
      }
    }
    
    async function loadEBProfile(mst) {
      if (!mst) return;
      try {
        const response = await fetch(/api/load-eb/);
        if (response.ok) {
          const data = await response.json();
          if (data.company) {
            document.getElementById('eb-company-name').value = data.company.name || '';
          }
          if (data.reporting_period) {
            document.getElementById('eb-period').value = data.reporting_period || '';
          }
          if (data.financials) {
            const formatVND = val => val ? (val / 1e9).toFixed(1) : '';
            document.getElementById('eb-ca').value = formatVND(data.financials.BS001);
            document.getElementById('eb-cl').value = formatVND(data.financials.BS002);
            document.getElementById('eb-ar').value = formatVND(data.financials.BS003);
            document.getElementById('eb-inv').value = formatVND(data.financials.BS004);
            document.getElementById('eb-ap').value = formatVND(data.financials.BS005);
            document.getElementById('eb-std').value = formatVND(data.financials.BS006);
            document.getElementById('eb-tl').value = formatVND(data.financials.BS007);
            document.getElementById('eb-equity').value = formatVND(data.financials.BS008);
            document.getElementById('eb-revenue').value = formatVND(data.financials.IS001);
            document.getElementById('eb-gp').value = formatVND(data.financials.IS002);
            document.getElementById('eb-ebit').value = formatVND(data.financials.IS003);
            document.getElementById('eb-interest').value = formatVND(data.financials.IS004);
            document.getElementById('eb-np').value = formatVND(data.financials.IS005);
            document.getElementById('eb-ocf').value = formatVND(data.financials.CF001);
            document.getElementById('eb-icf').value = formatVND(data.financials.CF002);
            document.getElementById('eb-fcf').value = formatVND(data.financials.CF003);
          }
        }
      } catch (err) {
        console.error(err);
      }
    }
'''
end_script = html.rfind('</script>')
if end_script != -1:
    html = html[:end_script] + save_load_js + html[end_script:]

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
