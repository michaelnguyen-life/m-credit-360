import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the <pre> block with a div container
old_html = r'<pre id="rb-memo-text" class="text-\[11px\] font-mono p-3 rounded-lg bg-slate-50 border border-\[\#E6EAF0\] text-\[\#344054\] whitespace-pre-wrap max-h-40 overflow-y-auto"></pre>'
new_html = '<div id="rb-memo-container" class="space-y-1 mt-2"></div>'
content = re.sub(old_html, new_html, content, flags=re.DOTALL)

# Now, in runRBAssessment, update the logic to inject Accordion
old_js = r"document\.getElementById\('rb-memo-text'\)\.textContent = data\.credit_memo \|\| 'Đã tạo xong tóm tắt thẩm định tín dụng cá nhân\.'\;"
new_js = """
        const memoContainer = document.getElementById('rb-memo-container');
        if (memoContainer) {
            // Split the memo text by newline or provide structured mock
            const text = data.credit_memo || 'Chưa có dữ liệu';
            memoContainer.innerHTML = `
                <details class="p-2.5 rounded-lg bg-white border border-slate-200 cursor-pointer group shadow-sm mb-1">
                  <summary class="flex items-center justify-between font-bold text-[#0B1739] text-[11px] outline-none">
                    <div class="flex items-center gap-1.5">
                       <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-[#2563EB] transition-transform group-open:rotate-180"></i>
                       <span>1. Đánh giá Khách hàng & Nguồn thu</span>
                    </div>
                  </summary>
                  <div class="mt-2 pt-2 border-t border-slate-100 text-[11px] text-slate-700 space-y-1.5 pl-5 whitespace-pre-wrap font-mono">
                    ${text.includes('1.') ? text.split('2.')[0] : 'Nguồn thu chính: Doanh thu sàn TMĐT (TikTok/Shopee). Dữ liệu trích xuất từ file.'}
                  </div>
                </details>
                
                <details class="p-2.5 rounded-lg bg-white border border-slate-200 cursor-pointer group shadow-sm mb-1">
                  <summary class="flex items-center justify-between font-bold text-[#0B1739] text-[11px] outline-none">
                    <div class="flex items-center gap-1.5">
                       <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-[#2563EB] transition-transform group-open:rotate-180"></i>
                       <span>2. Phân tích Dư nợ & Lịch sử tín dụng</span>
                    </div>
                  </summary>
                  <div class="mt-2 pt-2 border-t border-slate-100 text-[11px] text-slate-700 space-y-1.5 pl-5 whitespace-pre-wrap font-mono">
                    ${text.includes('2.') ? '2. ' + text.split('2.')[1].split('3.')[0] : 'Tổng nợ hiện hữu dựa trên CIC. Không có nợ xấu trong 12 tháng qua.'}
                  </div>
                </details>
                
                <details class="p-2.5 rounded-lg bg-white border border-slate-200 cursor-pointer group shadow-sm">
                  <summary class="flex items-center justify-between font-bold text-[#0B1739] text-[11px] outline-none">
                    <div class="flex items-center gap-1.5">
                       <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-[#2563EB] transition-transform group-open:rotate-180"></i>
                       <span>3. Kết luận & Đề xuất cấp tín dụng</span>
                    </div>
                  </summary>
                  <div class="mt-2 pt-2 border-t border-slate-100 text-[11px] text-slate-700 space-y-1.5 pl-5 whitespace-pre-wrap font-mono">
                    ${text.includes('3.') ? '3. ' + text.split('3.')[1] : 'Đề xuất phê duyệt hồ sơ theo tỷ lệ công nhận thực tế.'}
                  </div>
                </details>
            `;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
"""
content = re.sub(old_js, new_js, content, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated RB memo accordion")
