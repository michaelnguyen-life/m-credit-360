import re

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update saveDraftNotification and add loadDraft logic
save_logic = '''
    // ==========================================
    // ADDED JS FOR SAVING DRAFT & SIDEBAR
    // ==========================================

    function saveDraftNotification() {
        // Collect current data
        const draft = {
            taxId: document.getElementById('eb-tax-id')?.value,
            companyName: document.getElementById('eb-company-name')?.value,
            period: document.getElementById('eb-period')?.value,
            revenue: document.getElementById('eb-revenue')?.value,
            ebit: document.getElementById('eb-ebit')?.value,
            ca: document.getElementById('eb-ca')?.value,
            cl: document.getElementById('eb-cl')?.value,
            ar: document.getElementById('eb-ar')?.value,
            inv: document.getElementById('eb-inv')?.value,
            ap: document.getElementById('eb-ap')?.value,
            equity: document.getElementById('eb-equity')?.value,
            interest: document.getElementById('eb-interest')?.value,
            principal: document.getElementById('eb-principal')?.value,
            p039_contract: document.getElementById('eb-p039-contract')?.value,
            p039_loan: document.getElementById('eb-p039-loan')?.value,
            kpi_nwc: document.getElementById('kpi-nwc')?.textContent,
            kpi_dscr: document.getElementById('kpi-dscr')?.textContent,
            kpi_icr: document.getElementById('kpi-icr')?.textContent,
            kpi_p039: document.getElementById('kpi-p039')?.textContent,
            decision: document.getElementById('eb-decision-text')?.textContent
        };
        localStorage.setItem('mcredit_draft', JSON.stringify(draft));
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
        const statusSpan = document.querySelector('span:has(> span.bg-\\[\\#00A86B\\])');
        if (statusSpan) {
            statusSpan.innerHTML = <span class="w-1.5 h-1.5 rounded-full bg-[#00A86B]"></span><span>Đã lưu nháp </span>;
        }
        showToast(Đã lưu nháp lúc , 'info');
    }

    function loadDraft() {
        const saved = localStorage.getItem('mcredit_draft');
        if (saved) {
            try {
                const draft = JSON.parse(saved);
                if (draft.taxId) {
                    document.getElementById('eb-empty-state')?.classList.add('hidden');
                    document.getElementById('eb-results-container')?.classList.remove('hidden');
                }
                
                const setVal = (id, val) => { const el = document.getElementById(id); if (el && val) el.value = val; };
                const setTxt = (id, val) => { const el = document.getElementById(id); if (el && val) el.textContent = val; };
                
                setVal('eb-tax-id', draft.taxId);
                setVal('eb-company-name', draft.companyName);
                setVal('eb-period', draft.period);
                setVal('eb-revenue', draft.revenue);
                setVal('eb-ebit', draft.ebit);
                setVal('eb-ca', draft.ca);
                setVal('eb-cl', draft.cl);
                setVal('eb-ar', draft.ar);
                setVal('eb-inv', draft.inv);
                setVal('eb-ap', draft.ap);
                setVal('eb-equity', draft.equity);
                setVal('eb-interest', draft.interest);
                setVal('eb-principal', draft.principal);
                setVal('eb-p039-contract', draft.p039_contract);
                setVal('eb-p039-loan', draft.p039_loan);
                
                setTxt('kpi-nwc', draft.kpi_nwc);
                setTxt('kpi-dscr', draft.kpi_dscr);
                setTxt('kpi-icr', draft.kpi_icr);
                setTxt('kpi-p039', draft.kpi_p039);
                if (draft.decision) {
                    setTxt('eb-decision-text', draft.decision);
                }
            } catch (e) {
                console.error("Draft load error", e);
            }
        }
    }

    // Replace old saveDraftNotification if it exists in another script block
    window.saveDraftNotification = saveDraftNotification;
'''

content = re.sub(r'function saveDraftNotification.*?\}', '', content, flags=re.DOTALL)
content = content.replace('// Auto initialize on load', save_logic + '\n    // Auto initialize on load')
content = content.replace('runEBAssessment();', 'loadDraft();\n      runEBAssessment();')

# 2. Add generic section HTML for sidebar items to navigate to
generic_section_html = '''
      <!-- ==================== GENERIC SECTION ==================== -->
      <div id="section-generic" class="hidden execuTive-card p-8 text-center border-dashed border-2 border-slate-300 space-y-3 mt-4">
        <div class="w-12 h-12 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto">
          <i data-lucide="layout" class="w-6 h-6"></i>
        </div>
        <h3 id="generic-title" class="text-sm font-bold text-[#0B1739] uppercase tracking-wide">MÔ ĐUN ĐANG XÂY DỰNG</h3>
        <p class="text-xs text-[#667085] max-w-sm mx-auto">
          Tính năng này đã được ghi nhận trong phiên bản hiện tại và sẽ sớm được cập nhật. Bạn có thể quay lại trang Thẩm định AI để tiếp tục.
        </p>
      </div>
'''

content = content.replace('<!-- ==================== MAIN 3-COLUMN WORKSPACE (EB) ==================== -->', generic_section_html + '\n      <!-- ==================== MAIN 3-COLUMN WORKSPACE (EB) ==================== -->')

# 3. Add sidebar navigation logic
sidebar_logic = '''
    function setupSidebar() {
        const links = document.querySelectorAll('aside nav a');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                // Reset all links
                links.forEach(l => {
                    l.className = 'flex items-center gap-2.5 px-3 py-2 rounded-lg text-[#667085] hover:text-[#0B1739] hover:bg-slate-50 font-medium transition';
                    const icon = l.querySelector('i');
                    if (icon) icon.className = icon.className.replace('text-[#FF5A00]', '');
                });
                
                // Set active link
                link.className = 'flex items-center gap-2.5 px-3 py-2 rounded-lg bg-[#FFF4EB] text-[#FF5A00] font-bold transition border border-orange-100';
                const icon = link.querySelector('i');
                if (icon) icon.className += ' text-[#FF5A00]';
                
                // Show hide sections
                const href = link.getAttribute('href');
                const genericSec = document.getElementById('section-generic');
                const ebSec = document.getElementById('section-eb');
                const titleSec = document.getElementById('generic-title');
                
                if (href === '#assessment') {
                    genericSec.classList.add('hidden');
                    ebSec.classList.remove('hidden');
                } else {
                    ebSec.classList.add('hidden');
                    genericSec.classList.remove('hidden');
                    titleSec.textContent = 'MÔ ĐUN: ' + link.textContent.trim().toUpperCase();
                }
            });
        });
    }
'''

content = content.replace('// Auto initialize on load', sidebar_logic + '\n    // Auto initialize on load')
content = content.replace('loadDraft();', 'setupSidebar();\n      loadDraft();')

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Draft & Sidebar")
