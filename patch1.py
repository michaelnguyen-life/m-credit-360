import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean up Sidebar
sidebar_pattern = r'<nav class="flex-1 px-4 space-y-1 overflow-y-auto">.*?</nav>'
new_sidebar = """<nav class="flex-1 px-4 space-y-1 overflow-y-auto">
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-orange-50 text-[#FF5A00] font-bold text-sm transition">
          <i data-lucide="shield-check" class="w-5 h-5"></i>
          Thẩm định AI
        </a>
        <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[#667085] hover:bg-slate-50 font-medium text-sm transition">
          <i data-lucide="history" class="w-5 h-5"></i>
          Lịch sử thẩm định
        </a>
      </nav>"""
content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)

# 2. Add MST Search Button & Mock Logic
# Find the MST input field
mst_pattern = r'<label class="block text-xs font-bold text-\[\#0B1739\] mb-1\.5">Mã số thuế \(MST\).*?</label>\s*<input id="eb-tax-id".*?>'
# We'll replace it with a flex container holding the input and a search button
mst_new = """<label class="block text-xs font-bold text-[#0B1739] mb-1.5">Mã số thuế (MST) <span class="text-red-500">*</span></label>
                <div class="flex gap-2">
                  <input id="eb-tax-id" type="text" placeholder="Nhập MST (10 số)..." class="executive-input flex-1 px-3 py-2 text-sm" />
                  <button type="button" onclick="mockMSTLookup()" class="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-200 transition" title="Tra cứu MST">
                    <i data-lucide="search" class="w-4 h-4"></i>
                  </button>
                </div>"""
content = re.sub(r'<label class="block text-xs font-bold text-\[\#0B1739\] mb-1\.5">Mã số thuế \(MST\).*?</label>\s*<input id="eb-tax-id".*?/>', mst_new, content, flags=re.DOTALL)

# Add the JS for mockMSTLookup
js_mock_mst = """
    function mockMSTLookup() {
        const mst = document.getElementById('eb-tax-id').value.trim();
        const nameInput = document.getElementById('eb-company-name');
        if(!mst) { showToast('Vui lòng nhập MST trước khi tra cứu', 'error'); return; }
        showToast('Đang tra cứu cơ sở dữ liệu quốc gia...', 'info');
        setTimeout(() => {
            if (mst === '0101243150') nameInput.value = 'TẬP ĐOÀN TÂN HOÀNG MINH';
            else if (mst === '0300588569') nameInput.value = 'CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)';
            else if (mst === '0101010101') nameInput.value = 'CÔNG TY CỔ PHẦN TẬP ĐOÀN FLC';
            else nameInput.value = 'CÔNG TY CỔ PHẦN ĐẦU TƯ KHANG THỊNH';
            showToast('Tra cứu thành công!', 'info');
        }, 800);
    }
"""
content = content.replace("function focusManualEntry() {", js_mock_mst + "\n    function focusManualEntry() {")

# 3. Rename "Stress test" to "Kiểm tra dòng tiền"
content = content.replace("Stress-test dòng tiền", "Kiểm tra dòng tiền: kiểm tra sao kê & báo cáo tiền về tài khoản MSB đạt % doanh thu")
content = content.replace("Stress Test", "KT Dòng tiền")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
