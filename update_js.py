import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hardcoded OSINT and Cross-sell in runEBAssessment
hardcoded_start = html.find('// Mockup OSINT 360 values')
hardcoded_end = html.find('const flagsList = document.getElementById(\'eb-flags-list\');')

new_logic = '''
        // Fetch OSINT from API based on MST (simulated server logic)
        const taxId = document.getElementById('eb-tax-id').value;
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

html = html[:hardcoded_start] + new_logic + html[hardcoded_end:]

# Add auto-load when MST loses focus
mst_input = 'id="eb-tax-id" type="text" placeholder="Ví dụ: 0101234567"'
mst_input_new = 'id="eb-tax-id" type="text" placeholder="Ví dụ: 0101234567" onblur="loadEBProfile(this.value)"'
html = html.replace(mst_input, mst_input_new)

# Add Save/Load JS functions
save_load_js = '''
    // ==========================================
    // SAVE / LOAD PROFILES
    // ==========================================
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
          BS008: parseVND(document.getElementById('eb-te').value),
          IS001: parseVND(document.getElementById('eb-rev').value),
          IS002: parseVND(document.getElementById('eb-gp').value),
          IS003: parseVND(document.getElementById('eb-ebit').value),
          IS004: parseVND(document.getElementById('eb-ie').value),
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
            document.getElementById('eb-te').value = formatVND(data.financials.BS008);
            document.getElementById('eb-rev').value = formatVND(data.financials.IS001);
            document.getElementById('eb-gp').value = formatVND(data.financials.IS002);
            document.getElementById('eb-ebit').value = formatVND(data.financials.IS003);
            document.getElementById('eb-ie').value = formatVND(data.financials.IS004);
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
html = html[:end_script] + save_load_js + html[end_script:]

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
