import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change grid to flex-col
content = content.replace('<div id="eb-cross-list" class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">', '<div id="eb-cross-list" class="flex flex-col gap-2 text-xs">')

# We inject the accordion JS by replacing the previous static container innerHTML update.
# Wait, let's find the current JS inside runEBAssessment:
old_js = "const csContainer = document.querySelector('.grid.grid-cols-3.gap-3');"
new_js = """
                const csContainer = document.getElementById('eb-cross-list');
                if (csContainer) {
                    csContainer.innerHTML = `
                    <details class="p-2.5 rounded-lg bg-orange-50 border border-orange-200 cursor-pointer group mb-1">
                      <summary class="flex items-center justify-between font-bold text-[#0B1739] text-xs outline-none">
                        <div class="flex items-center gap-2">
                           <i data-lucide="chevron-down" class="w-4 h-4 text-[#FF5A00] transition-transform group-open:rotate-180"></i>
                           <span>1. Cơ hội: Tài trợ Phải thu & Phân tích Đầu ra</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-orange-100 text-[#FF5A00]">P1</span>
                            <span class="font-mono text-[#FF5A00]">~ ${cs1} Tỷ</span>
                        </div>
                      </summary>
                      <div class="mt-2 pt-2 border-t border-orange-100 text-[11px] text-slate-700 space-y-1.5 pl-6">
                        <p><strong>Cơ sở phân tích:</strong> Tối ưu dòng tiền từ khoản phải thu ${(ar/1e9).toFixed(1)} Tỷ.</p>
                        <p><strong>Phân tích Đối tác Đầu ra (Top Người mua):</strong></p>
                        <ul class="list-disc pl-4 text-orange-900">
                          <li>Công ty CP Xây dựng Hòa Bình (Tỷ trọng 35%)</li>
                          <li>Tập đoàn Vingroup (Tỷ trọng 25%)</li>
                          <li>Công ty TNHH Thương mại ABC (Tỷ trọng 15%)</li>
                        </ul>
                      </div>
                    </details>
                    
                    <details class="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 cursor-pointer group mb-1">
                      <summary class="flex items-center justify-between font-bold text-[#0B1739] text-xs outline-none">
                        <div class="flex items-center gap-2">
                           <i data-lucide="chevron-down" class="w-4 h-4 text-[#027A48] transition-transform group-open:rotate-180"></i>
                           <span>2. Cơ hội: Tài trợ SCF / L/C & Phân tích Đầu vào</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-100 text-[#027A48]">P2</span>
                            <span class="font-mono text-[#027A48]">~ ${cs2} Tỷ</span>
                        </div>
                      </summary>
                      <div class="mt-2 pt-2 border-t border-emerald-100 text-[11px] text-slate-700 space-y-1.5 pl-6">
                        <p><strong>Cơ sở phân tích:</strong> Thanh toán chuỗi cung ứng dựa trên doanh thu ${(rev/1e9).toFixed(1)} Tỷ.</p>
                        <p><strong>Phân tích Đối tác Đầu vào (Top Nhà cung cấp):</strong></p>
                        <ul class="list-disc pl-4 text-emerald-900">
                          <li>Công ty CP Thép Hòa Phát (Tỷ trọng 40%) -> Mở L/C nội địa</li>
                          <li>Nhà cung cấp Vật liệu Tín Phát (Tỷ trọng 20%)</li>
                        </ul>
                      </div>
                    </details>
                    `;
                    if (typeof lucide !== 'undefined') lucide.createIcons();
                }
"""

content = content.replace(old_js, new_js)

# Clear static HTML inside eb-cross-list
pattern = r'<div id="eb-cross-list" class="flex flex-col gap-2 text-xs">.*?</div>\s*</div>\s*<!-- M-CREDIT AI Insight -->'
replacement = r'<div id="eb-cross-list" class="flex flex-col gap-2 text-xs"></div>\n            </div>\n            <!-- M-CREDIT AI Insight -->'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
