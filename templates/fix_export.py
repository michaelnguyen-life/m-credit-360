with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
old_func = re.search(r'async function exportDocxMemo\(\) \{.*?(?=\n    \}|\n\n)', content, flags=re.DOTALL)

new_func = '''async function exportDocxMemo() {
        const btn = document.getElementById('btn-export-docx');
        if (btn.disabled) return;
        
        btn.disabled = true;
        const originalHtml = btn.innerHTML;
        btn.innerHTML = <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>Đang tạo tờ trình...</span>;
        if (typeof lucide !== 'undefined') lucide.createIcons();

        try {
            const taxId = document.getElementById('eb-tax-id').value || "mock";
            
            const parseNum = (id) => {
                const el = document.getElementById(id);
                if (!el || !el.value) return null;
                const v = el.value.replace(/[^0-9-]/g, '');
                return v ? parseFloat(v) : null;
            };

            const payload = {
                assessment_id: "EB-" + Date.now(),
                company: {
                    tax_id: taxId,
                    name: document.getElementById('eb-company-name').value
                },
                financials: {
                    IS_REVENUE: parseNum('eb-revenue'),
                    IS_EBIT: parseNum('eb-ebit'),
                    BS_CURRENT_ASSETS: parseNum('eb-ca'),
                    BS_CURRENT_LIABILITIES: parseNum('eb-cl'),
                    BS_TRADE_RECEIVABLES: parseNum('eb-ar'),
                    BS_INVENTORY: parseNum('eb-inv'),
                    BS_TRADE_PAYABLES: parseNum('eb-ap'),
                    BS_EQUITY: parseNum('eb-equity'),
                    IS_INTEREST_EXPENSE: parseNum('eb-interest')
                },
                debt_service: {
                    principal_due: parseNum('eb-principal')
                },
                product_039: {
                    contract_value: parseNum('eb-p039-contract'),
                    loan_request_amount: parseNum('eb-p039-loan'),
                    customer_equity: parseNum('eb-equity')
                }
            };

            const res = await fetch('/build-memo-docx', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
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
    }'''

content = content.replace(old_func.group(0), new_func)

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated exportDocxMemo")
