import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Modify the Modal to support MST/CCCD and the search button
modal_mst_pattern = r'<label class="block text-\[\#667085\] font-medium text-\[11px\] mb-1">Mã số thuế \(MST\)</label>\s*<input id="modal-tax-id" type="text" placeholder="Nhập MST..." class="w-full px-2\.5 py-1\.5 border border-\[\#D0D5DD\] rounded-lg text-xs outline-none focus:border-\[\#FF5A00\]" />'

new_modal_mst = """<label class="block text-[#667085] font-medium text-[11px] mb-1">Mã số thuế (MST) / CCCD (KHCN)</label>
          <div class="flex gap-2">
            <input id="modal-tax-id-input" type="text" placeholder="Nhập MST / CCCD..." class="w-full px-2.5 py-1.5 border border-[#D0D5DD] rounded-lg text-xs outline-none focus:border-[#FF5A00]" />
            <button type="button" onclick="mockModalLookup()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg border border-slate-200 transition" title="Tra cứu">
              <i data-lucide="search" class="w-3.5 h-3.5"></i>
            </button>
          </div>"""

content = re.sub(modal_mst_pattern, new_modal_mst, content, flags=re.DOTALL)

# Add mockModalLookup function
js_lookup = """
    function mockModalLookup() {
        const mst = document.getElementById('modal-tax-id-input').value.trim();
        const nameInput = document.getElementById('modal-company-name-input');
        if(!mst) { showToast('Vui lòng nhập MST hoặc CCCD trước khi tra cứu', 'error'); return; }
        showToast('Đang tra cứu dữ liệu quốc gia...', 'info');
        setTimeout(() => {
            if (mst === '0101243150') nameInput.value = 'TẬP ĐOÀN TÂN HOÀNG MINH';
            else if (mst === '0300588569') nameInput.value = 'CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)';
            else if (mst === '0101010101') nameInput.value = 'CÔNG TY CỔ PHẦN TẬP ĐOÀN FLC';
            else if (mst.length === 12) nameInput.value = 'PHẠM THANH BÌNH (KHCN)'; // Giả lập CCCD
            else nameInput.value = 'CÔNG TY CỔ PHẦN ĐẦU TƯ KHANG THỊNH';
            showToast('Tra cứu thành công!', 'info');
        }, 800);
    }
"""
content = content.replace("function openNewCustomerModal() {", js_lookup + "\n    function openNewCustomerModal() {")

# Also need to fix the input ID for company name in the modal
content = content.replace('id="modal-company-name"', 'id="modal-company-name-input"')

# The save logic of the modal uses `modal-tax-id` and `modal-company-name`. I should rename my inputs to match, or change the save logic.
# Let's change my inputs to match exactly:
content = content.replace('id="modal-tax-id-input"', 'id="modal-tax-id"')
content = content.replace('id="modal-company-name-input"', 'id="modal-company-name"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated modal")
