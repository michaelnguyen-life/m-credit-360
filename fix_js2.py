import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

js_insert_point = html.find('lucide.createIcons();\\n      } catch (err) {')
# Wait, let's just find the exact string without \n
js_insert_point = html.find('        lucide.createIcons();')
if js_insert_point != -1:
    # We want to inject it before this line, but make sure it's inside the try block
    # Actually, the original code had:
    #         lucide.createIcons();
    #       } catch (err) {
    # So finding '        lucide.createIcons();' is good!
    # Wait, there might be multiple. Let's find the one before catch (err).
    insert_str = '        lucide.createIcons();\\n      } catch (err) {'
    
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
    
    # We will just find the right lucide.createIcons();
    lines = html.split('\\n')
    for i, line in enumerate(lines):
        if 'lucide.createIcons();' in line and 'catch (err)' in lines[i+1]:
            lines.insert(i, new_osint_js)
            break
            
    html = '\\n'.join(lines)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
