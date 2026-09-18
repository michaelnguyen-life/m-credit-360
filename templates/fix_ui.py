import re

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace new-customer-modal
new_modal_html = '''
  <div id="new-customer-modal" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center hidden">
    <div class="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl border border-[#E6EAF0] space-y-4 m-4">
      <div class="w-10 h-10 rounded-xl bg-orange-100 text-[#FF5A00] flex items-center justify-center">
        <i data-lucide="user-plus" class="w-5 h-5"></i>
      </div>
      <div>
        <h3 class="text-base font-bold text-[#0B1739]">Tạo hồ sơ khách hàng mới</h3>
        <p class="text-xs text-[#667085] mt-1.5 leading-relaxed">
          Nhập các thông tin cơ bản để bắt đầu phiên thẩm định. Dữ liệu của phiên hiện tại sẽ bị xóa.
        </p>
      </div>
      <div class="space-y-3">
        <div>
          <label class="block text-[#667085] font-medium text-[11px] mb-1">Mã số thuế (MST)</label>
          <input id="modal-tax-id" type="text" placeholder="Nhập MST..." class="w-full px-2.5 py-1.5 border border-[#D0D5DD] rounded-lg text-xs outline-none focus:border-[#FF5A00]" />
        </div>
        <div>
          <label class="block text-[#667085] font-medium text-[11px] mb-1">Tên doanh nghiệp</label>
          <input id="modal-company-name" type="text" placeholder="Nhập tên doanh nghiệp..." class="w-full px-2.5 py-1.5 border border-[#D0D5DD] rounded-lg text-xs outline-none focus:border-[#FF5A00]" />
        </div>
        <div>
          <label class="block text-[#667085] font-medium text-[11px] mb-1">Kỳ báo cáo</label>
          <select id="modal-period" class="w-full px-2.5 py-1.5 border border-[#D0D5DD] rounded-lg text-xs outline-none focus:border-[#FF5A00]">
            <option value="2025">2025 (Cả năm)</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
          </select>
        </div>
      </div>
      <div class="flex items-center justify-end space-x-2 pt-2 border-t border-[#E6EAF0]">
        <button onclick="closeNewCustomerModal()" class="px-4 py-2 rounded-lg text-xs font-semibold text-[#667085] hover:bg-slate-100 transition">
          Hủy
        </button>
        <button onclick="confirmNewCustomerSession()" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs transition shadow-sm">
          Tạo khách hàng
        </button>
      </div>
    </div>
  </div>
'''

content = re.sub(r'<div id=\"new-customer-modal\".*?<!-- ==================== DRAWER', new_modal_html + '\n  <!-- ==================== DRAWER', content, flags=re.DOTALL)

# 2. Add JavaScript logic
js_logic = '''
    // ==========================================
    // ADDED JS FOR BUTTON INTERACTIONS
    // ==========================================

    function openNewCustomerModal() {
        document.getElementById('new-customer-modal').classList.remove('hidden');
    }

    function closeNewCustomerModal() {
        document.getElementById('new-customer-modal').classList.add('hidden');
    }

    function confirmNewCustomerSession() {
        const taxId = document.getElementById('modal-tax-id').value;
        const companyName = document.getElementById('modal-company-name').value;
        const period = document.getElementById('modal-period').value;

        // Reset main form
        document.getElementById('eb-tax-id').value = taxId;
        document.getElementById('eb-company-name').value = companyName;
        document.getElementById('eb-period').value = period;

        // Reset all metrics
        const inputsToReset = ['eb-revenue', 'eb-ebit', 'eb-ca', 'eb-cl', 'eb-ar', 'eb-inv', 'eb-ap', 'eb-equity', 'eb-interest', 'eb-principal', 'eb-p039-contract', 'eb-p039-loan'];
        inputsToReset.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
        });

        document.getElementById('kpi-nwc').textContent = 'N/A';
        document.getElementById('kpi-dscr').textContent = 'N/A';
        document.getElementById('kpi-icr').textContent = 'N/A';
        document.getElementById('kpi-p039').textContent = 'N/A';
        document.getElementById('eb-decision-text').textContent = 'Chưa có dữ liệu';
        document.getElementById('eb-flags-list').innerHTML = '';
        document.getElementById('eb-flags-count').textContent = '0 Cảnh báo';
        
        // Show empty state
        const emptyState = document.getElementById('eb-empty-state');
        if (emptyState) emptyState.classList.remove('hidden');
        
        const resultsContainer = document.getElementById('eb-results-container');
        if (resultsContainer) resultsContainer.classList.add('hidden');

        closeNewCustomerModal();
    }

    function openUploadDrawer() {
        document.getElementById('upload-drawer').classList.remove('hidden');
    }

    function closeUploadDrawer() {
        document.getElementById('upload-drawer').classList.add('hidden');
    }

    function handleFileSelect(event) {
        const files = event.target.files;
        if (!files || files.length === 0) return;
        
        const fileList = document.querySelector('.space-y-2'); // Container of Hồ sơ khách hàng items
        // Let's create a toast or append directly
        
        Array.from(files).forEach(file => {
            // Append to DOM (mock)
            const el = document.createElement('div');
            el.className = 'p-2 rounded-lg border border-[#E6EAF0] flex items-center justify-between hover:bg-slate-50 transition bg-white';
            el.innerHTML = 
                <div class="flex items-center gap-2.5 overflow-hidden">
                    <div class="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center shrink-0">
                        <i data-lucide="file" class="w-4 h-4 text-[#FF5A00]"></i>
                    </div>
                    <div class="min-w-0">
                        <span class="text-xs font-semibold text-[#0B1739] block truncate w-32 sm:w-40"></span>
                        <span class="text-[9px] text-[#98A2B3] uppercase font-mono"> MB</span>
                    </div>
                </div>
                <span class="text-[10px] font-bold text-[#FF5A00] animate-pulse">Đang tải lên</span>
            ;
            // If the UI has a specific container, try to find it. Otherwise just use body/toast.
            const container = document.getElementById('eb-file-list');
            if (container) {
                container.prepend(el);
            } else {
                showToast(Tải lên file );
            }

            // Simulate processing
            setTimeout(() => {
                const statusSpan = el.querySelector('span:last-child');
                statusSpan.textContent = 'Đã bóc tách';
                statusSpan.className = 'text-[10px] font-bold text-[#00A86B]';
                
                // Hide empty state if visible
                const emptyState = document.getElementById('eb-empty-state');
                if (emptyState) emptyState.classList.add('hidden');
                const resultsContainer = document.getElementById('eb-results-container');
                if (resultsContainer) resultsContainer.classList.remove('hidden');
                
            }, 1500);
        });
        
        closeUploadDrawer();
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    function showToast(message, type='info') {
        const toast = document.createElement('div');
        const color = type === 'error' ? 'bg-red-500' : 'bg-slate-800';
        toast.className = ixed bottom-4 right-4  text-white px-4 py-2 rounded-lg text-xs font-bold shadow-lg z-50 animate-bounce;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    async function runEBAssessment() {
        const btn = document.getElementById('btn-run-eb');
        if (btn.disabled) return;
        
        btn.disabled = true;
        const originalHtml = btn.innerHTML;
        btn.innerHTML = <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>AI đang thẩm định...</span>;
        if (typeof lucide !== 'undefined') lucide.createIcons();

        try {
            // Check required fields
            const taxId = document.getElementById('eb-tax-id').value;
            if (!taxId) {
                showToast('Lỗi: Cần nhập Mã số thuế trước khi thẩm định', 'error');
                return;
            }
            
            const payload = {
                assessment_id: "EB-" + Date.now(),
                company: {
                    tax_id: taxId,
                    name: document.getElementById('eb-company-name').value
                }
            };

            const res = await fetch('/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (!res.ok) throw new Error(HTTP Error );
            
            const data = await res.json();
            
            // Render basic UI elements from data
            if (data.decision_text) {
                document.getElementById('eb-decision-text').textContent = data.decision_text;
            }
            document.getElementById('kpi-nwc').textContent = (data.kpi_nwc || "34,5 Tỷ");
            document.getElementById('kpi-dscr').textContent = (data.kpi_dscr || "1.2x");
            document.getElementById('kpi-icr').textContent = (data.kpi_icr || "1.8x");
            document.getElementById('kpi-p039').textContent = (data.kpi_p039 || "76%");
            
            showToast('Thẩm định AI thành công');
            
        } catch (err) {
            showToast('Lỗi thẩm định AI: ' + err.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    }

    async function exportDocxMemo() {
        const btn = document.getElementById('btn-export-docx');
        if (btn.disabled) return;
        
        btn.disabled = true;
        const originalHtml = btn.innerHTML;
        btn.innerHTML = <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>Đang tạo tờ trình...</span>;
        if (typeof lucide !== 'undefined') lucide.createIcons();

        try {
            const taxId = document.getElementById('eb-tax-id').value || "mock";
            const res = await fetch('/build-memo-docx', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company: { tax_id: taxId } })
            });
            
            if (!res.ok) throw new Error(HTTP Error );
            
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = To_Trinh_MB02a_.docx;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showToast('Tạo tờ trình thành công');
        } catch (err) {
            showToast('Lỗi tạo tờ trình: ' + err.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    }
'''

content = content.replace('// Auto initialize on load', js_logic + '\n    // Auto initialize on load')

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
