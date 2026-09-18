import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add EB Cross-sell Button
eb_btn_pattern = r'<button onclick="runEBAssessment\(\)" id="btn-run-eb" class="px-4 py-2 rounded-lg bg-\[\#FF5A00\] hover:bg-\[\#EA4E00\] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">\s*<i data-lucide="play" class="w-3\.5 h-3\.5 fill-current"></i>\s*<span>CHẠY THẨM ĐỊNH AI 360°</span>\s*</button>'
eb_new_btn = """<button onclick="runEBAssessment()" id="btn-run-eb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            <span>CHẠY THẨM ĐỊNH AI 360°</span>
          </button>
          <button onclick="runEBCrossSell()" id="btn-eb-cross-sell" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="coins" class="w-3.5 h-3.5"></i>
            <span>TÌM KIẾM CƠ HỘI CROSS SELL</span>
          </button>"""
content = re.sub(eb_btn_pattern, eb_new_btn, content, flags=re.DOTALL)

# 2. Add RB Cross-sell Button
rb_btn_pattern = r'<button onclick="runRBAssessment\(\)" id="btn-run-rb" class="px-4 py-2 rounded-lg bg-\[\#FF5A00\] hover:bg-\[\#EA4E00\] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">\s*<i data-lucide="play" class="w-3\.5 h-3\.5 fill-current"></i>\s*<span>CHẠY THẨM ĐỊNH KHCN \(RB\)</span>\s*</button>'
rb_new_btn = """<button onclick="runRBAssessment()" id="btn-run-rb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            <span>CHẠY THẨM ĐỊNH KHCN (RB)</span>
          </button>
          <button onclick="runRBCrossSell()" id="btn-rb-cross-sell" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="coins" class="w-3.5 h-3.5"></i>
            <span>TÌM KIẾM CƠ HỘI CROSS SELL</span>
          </button>"""
content = re.sub(rb_btn_pattern, rb_new_btn, content, flags=re.DOTALL)

# 3. Wrap EB Cross-sell panel and hide it
eb_panel = r'<!-- Cross-Sell Alert Panel -->\s*<div class="executive-card p-3\.5 space-y-2">'
new_eb_panel = '<!-- Cross-Sell Alert Panel -->\n            <div id="eb-cross-sell-wrapper" class="executive-card p-3.5 space-y-2 hidden">'
content = re.sub(eb_panel, new_eb_panel, content)

# 4. Remove the DYNAMIC CROSS-SELL MOCK block from loadDraft (or anywhere)
mock_pattern = r'// DYNAMIC CROSS-SELL MOCK.*?if \(typeof lucide !== \'undefined\'\) lucide\.createIcons\(\);\s*\}'
content = re.sub(mock_pattern, '', content, flags=re.DOTALL)

# Remove any empty try catch left over if any
content = re.sub(r'try \{\s*\} catch\(e\) \{ console\.error\("Cross-sell update failed:", e\); \}', '', content)


# 5. Add runEBCrossSell and runRBCrossSell functions
js_code = """
    function runEBCrossSell() {
        const btn = document.getElementById('btn-eb-cross-sell');
        if (btn.disabled) return;
        btn.disabled = true;
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>ĐANG TÌM KIẾM CƠ HỘI...</span>`;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        
        setTimeout(() => {
            const parseNumSafe = (id) => {
                const el = document.getElementById(id);
                if (!el || !el.value) return 0;
                const v = el.value.replace(/[^0-9-]/g, '');
                return v ? parseFloat(v) : 0;
            };
            const rev = parseNumSafe('eb-revenue');
            const ar = parseNumSafe('eb-ar');
            
            const cs1 = ((ar * 0.3) / 1e9).toFixed(1);
            const cs2 = ((rev * 0.1) / 1e9).toFixed(1);
            const cs3 = ((rev * 0.05) / 1e9).toFixed(1);
            
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
            }
            document.getElementById('eb-cross-sell-wrapper').classList.remove('hidden');
            btn.innerHTML = originalHtml;
            btn.disabled = false;
            if (typeof lucide !== 'undefined') lucide.createIcons();
            showToast('Agent 3 (Cross-sell) đã phân tích xong dữ liệu Đối tác!', 'success');
        }, 1200);
    }

    function runRBCrossSell() {
        const btn = document.getElementById('btn-rb-cross-sell');
        if (btn.disabled) return;
        btn.disabled = true;
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>ĐANG TÌM KIẾM CƠ HỘI...</span>`;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        
        setTimeout(() => {
            const rbMemoContainer = document.getElementById('rb-memo-container');
            if (rbMemoContainer) {
                const newDetails = document.createElement('details');
                newDetails.className = "p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 cursor-pointer group shadow-sm mt-2 border-dashed";
                newDetails.innerHTML = `
                  <summary class="flex items-center justify-between font-bold text-[#0B1739] text-[11px] outline-none">
                    <div class="flex items-center gap-1.5">
                       <i data-lucide="coins" class="w-3.5 h-3.5 text-[#027A48]"></i>
                       <span class="text-[#027A48]">CƠ HỘI BÁN CHÉO (Phát hiện bởi Agent 3)</span>
                    </div>
                  </summary>
                  <div class="mt-2 pt-2 border-t border-emerald-100 text-[11px] text-slate-700 space-y-1.5 pl-5 font-mono">
                    <p>- <strong>Phát hành Thẻ Tín dụng:</strong> Lịch sử trả nợ tốt, đủ điều kiện thẻ Platinum.</p>
                    <p>- <strong>Bảo hiểm nhân thọ (Bancassurance):</strong> KH có dư nợ 450 Tr, cần bảo vệ khoản vay rủi ro tử kỳ.</p>
                    <p>- <strong>Mở TK VietQR:</strong> Dành cho cửa hàng TikTok Shop để nhận tiền trực tiếp.</p>
                  </div>
                `;
                rbMemoContainer.appendChild(newDetails);
            }
            btn.innerHTML = originalHtml;
            btn.disabled = false;
            if (typeof lucide !== 'undefined') lucide.createIcons();
            showToast('Agent 3 đã gợi ý 3 cơ hội Cross-sell cho Cá nhân!', 'success');
        }, 1000);
    }
"""

content = content.replace("function focusManualEntry() {", js_code + "\n    function focusManualEntry() {")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated UI")
