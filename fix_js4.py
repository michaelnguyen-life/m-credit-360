import io
import re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the broken JS that was appended at the end of the file in the previous failed run!
html = html.split('</html>')[0] + '</html>\n'

new_osint_js = '''
        // Dynamic OSINT & Cross-sell
        const osintData = data.osint || {
          tax_status: "Sạch (0đ)", tax_class: "text-green-600",
          bid_summary: "0 gói thầu", bid_class: "text-slate-500",
          bid_details: `<div class="text-slate-400 italic">Chưa ghi nhận lịch sử trúng thầu</div>`
        };
        
        document.getElementById('osint-tax').innerHTML = osintData.tax_status; 
        document.getElementById('osint-tax').className = `font-bold ${osintData.tax_class} font-mono`;
        document.getElementById('osint-bid-summary').innerHTML = osintData.bid_summary; 
        document.getElementById('osint-bid-summary').className = `font-bold ${osintData.bid_class}`;
        document.getElementById('osint-bid-details').innerHTML = osintData.bid_details;

        const crossList = document.getElementById('eb-cross-list');
        crossList.innerHTML = '';
        const deals = data.cross_sell_opportunities || [];
        let totalDeal = 0;
        document.getElementById('eb-cross-count').textContent = `${deals.length} Cơ hội chốt Deal`;
        
        if (deals.length === 0) {
            crossList.innerHTML = `<div class="p-2.5 rounded-lg bg-slate-50 text-slate-500 text-center border border-slate-200">Không tìm thấy cơ hội bán chéo.</div>`;
        } else {
            deals.forEach(deal => {
              totalDeal += deal.estimated_deal_size || 0;
              const prioClass = deal.priority === 'P1' ? 'bg-[#ECFDF3] text-[#027A48] border-[#A6F4C5]' : 'bg-[#EFF4FF] text-[#1D4ED8] border-[#B2CCFF]';
              crossList.innerHTML += `
                <details class="group bg-white rounded-lg border border-slate-200 overflow-hidden mb-2 shadow-sm">
                  <summary class="flex items-center justify-between p-2.5 cursor-pointer bg-slate-50 hover:bg-slate-100 transition list-none">
                    <div class="flex items-center gap-2">
                      <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-slate-400 group-open:-rotate-180 transition-transform"></i>
                      <span class="font-bold text-[#0B1739]">${deal.product}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-[9px] px-1.5 py-0.5 rounded border font-bold uppercase ${prioClass}">${deal.priority}</span>
                      <span class="font-mono font-bold text-[#FF5A00]">${(deal.estimated_deal_size / 1000000000).toFixed(1)} Tỷ</span>
                    </div>
                  </summary>
                  <div class="p-2.5 text-slate-600 bg-white border-t border-slate-100 leading-relaxed text-[11px]">
                    ${deal.reasoning}
                  </div>
                </details>
              `;
            });
        }
        document.getElementById('eb-cross-total').textContent = `Quy mô: ${(totalDeal / 1000000000).toFixed(1)} Tỷ`;
'''

target = "lucide.createIcons();"
parts = html.split(target)
if len(parts) >= 2:
    for i, part in enumerate(parts):
        if i + 1 < len(parts) and '} catch (err)' in parts[i+1][:50]:
            # Inject new_osint_js right before lucide.createIcons()
            parts[i] = parts[i] + new_osint_js
            break
            
    html = target.join(parts)
    
with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
