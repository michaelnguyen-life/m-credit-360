with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

injection = """
            // DYNAMIC CROSS-SELL MOCK
            try {
                const rev = parseNum('eb-revenue') || 0;
                const ar = parseNum('eb-ar') || 0;
                
                // Cross sell 1: Tai tro phai thu = 30% AR
                const cs1 = ((ar * 0.3) / 1e9).toFixed(1);
                // Cross sell 2: LC = 10% Rev
                const cs2 = ((rev * 0.1) / 1e9).toFixed(1);
                // Cross sell 3: Bao lanh = 5% Rev
                const cs3 = ((rev * 0.05) / 1e9).toFixed(1);
                
                const csContainer = document.querySelector('.grid.grid-cols-3.gap-3');
                if (csContainer) {
                    csContainer.innerHTML = `
                    <div class="p-2.5 rounded-lg bg-orange-50 border border-orange-100 relative overflow-hidden group hover:shadow-md transition">
                      <div class="absolute right-0 top-0 bg-orange-200 text-[#FF5A00] text-[8px] px-1.5 py-0.5 rounded-bl-lg font-bold">HOT</div>
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-[#0B1739] text-[11px]">Tài trợ Phải thu (QĐ.039)</span>
                        <span class="text-[8px] px-1 rounded bg-orange-100 text-[#FF5A00] font-bold">P1</span>
                      </div>
                      <p class="text-[10px] text-[#667085] leading-tight">Tối ưu dòng tiền phải thu</p>
                      <span class="font-black text-xs text-[#0B1739] font-mono block mt-1.5">~ ${cs1} Tỷ</span>
                    </div>
                    <div class="p-2.5 rounded-lg bg-emerald-50 border border-emerald-100 relative hover:shadow-md transition">
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-[#0B1739] text-[11px]">Tài trợ SCF / LC</span>
                        <span class="text-[8px] px-1 rounded bg-emerald-100 text-[#027A48] font-bold">P2</span>
                      </div>
                      <p class="text-[10px] text-[#667085] leading-tight">Thanh toán chuỗi cung ứng</p>
                      <span class="font-black text-xs text-[#0B1739] font-mono block mt-1.5">~ ${cs2} Tỷ</span>
                    </div>
                    <div class="p-2.5 rounded-lg bg-blue-50 border border-blue-100 relative hover:shadow-md transition">
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-[#0B1739] text-[11px]">Bảo lãnh Quốc tế</span>
                        <span class="text-[8px] px-1 rounded bg-blue-100 text-[#175CD3] font-bold">P3</span>
                      </div>
                      <p class="text-[10px] text-[#667085] leading-tight">Giao dịch xuyên biên giới</p>
                      <span class="font-black text-xs text-[#0B1739] font-mono block mt-1.5">~ ${cs3} Tỷ</span>
                    </div>`;
                }
            } catch(e) { console.error("Cross-sell update failed:", e); }
"""

for i in range(1765, 2300):
    if "document.getElementById('eb-results-container')?.classList.remove('hidden');" in lines[i]:
        lines.insert(i, injection)
        break

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
