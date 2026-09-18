with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def _parse_num(val): return float(str(val).replace('.', '').replace(',', '')) if val else None

new_run = '''
    async function runEBAssessment() {
        const btn = document.getElementById('btn-run-eb');
        if (btn.disabled) return;
        
        btn.disabled = true;
        const originalHtml = btn.innerHTML;
        btn.innerHTML = <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>AI đang thẩm định...</span>;
        if (typeof lucide !== 'undefined') lucide.createIcons();

        try {
            const taxId = document.getElementById('eb-tax-id').value;
            if (!taxId) {
                showToast('Lỗi: Cần nhập Mã số thuế trước khi thẩm định', 'error');
                return;
            }
            
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

            const res = await fetch('/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (!res.ok) throw new Error(HTTP Error );
            const data = await res.json();
            
            // Map Decision
            const outcomeMap = {
                'manual_review_required': 'Cảnh báo đỏ (Từ chối/Bổ sung)',
                'enhanced_due_diligence': 'Tái thẩm định đặc biệt',
                'conditional_review': 'Thẩm định có điều kiện',
                'no_rule_based_red_flag': 'Cho phép cấp tín dụng'
            };
            const decisionStr = data.preliminary_decision?.outcome;
            document.getElementById('eb-decision-text').textContent = outcomeMap[decisionStr] || 'Hoàn tất phân tích';
            
            if (decisionStr === 'manual_review_required') {
                document.getElementById('eb-decision-text').className = 'text-base font-black text-[#E53935]';
                document.getElementById('eb-decision-icon').className = 'w-10 h-10 rounded-xl bg-red-50 flex items-center justify-center text-[#E53935] shadow-sm flex-shrink-0';
                document.getElementById('eb-decision-icon').innerHTML = '<i data-lucide="alert-triangle" class="w-6 h-6"></i>';
                document.getElementById('eb-decision-banner').className = 'executive-card p-4 border border-[#FECDCA] bg-[#FEF3F2] flex items-center justify-between transition-all';
            } else {
                document.getElementById('eb-decision-text').className = 'text-base font-black text-[#027A48]';
                document.getElementById('eb-decision-icon').className = 'w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#00A86B] shadow-sm flex-shrink-0';
                document.getElementById('eb-decision-icon').innerHTML = '<i data-lucide="check-circle" class="w-6 h-6"></i>';
                document.getElementById('eb-decision-banner').className = 'executive-card p-4 border border-[#A6F4C5] bg-[#ECFDF3] flex items-center justify-between transition-all';
            }
            
            // Map Ratios
            const fmtVND = (v) => v ? (v / 1000000000).toFixed(2).replace('.', ',') + ' Tỷ' : 'N/A';
            const fmtRatio = (v) => v ? v.toFixed(2) + 'x' : 'N/A';
            const fmtPct = (v) => v ? (v * 100).toFixed(1) + '%' : 'N/A';
            
            document.getElementById('kpi-nwc').textContent = fmtVND(data.ratios?.nwc);
            document.getElementById('kpi-dscr').textContent = fmtRatio(data.ratios?.dscr);
            document.getElementById('kpi-icr').textContent = fmtRatio(data.ratios?.icr);
            document.getElementById('kpi-p039').textContent = fmtPct(data.product_039_evaluation?.eligibility_ratio);
            
            // Map Red Flags
            const flagsContainer = document.getElementById('eb-flags-list');
            const flags = data.red_flags || [];
            flagsContainer.innerHTML = '';
            let triggerCount = 0;
            
            flags.forEach(f => {
                if (!f.triggered) return;
                triggerCount++;
                const isCrit = f.severity === 'high';
                const fClass = isCrit ? 'bg-[#FEF3F2] border-[#FECDCA] text-[#B42318]' : 'bg-[#FFF9F2] border-[#FFE6CC] text-[#B54708]';
                const tagClass = isCrit ? 'bg-red-100 text-[#B42318]' : 'bg-amber-100 text-[#B54708]';
                const iconColor = isCrit ? 'text-[#E53935]' : 'text-[#F59E0B]';
                flagsContainer.innerHTML += 
                <div class="p-2.5 rounded-lg  border flex items-start gap-2.5 mb-2">
                  <i data-lucide="alert-circle" class="w-4 h-4  mt-0.5 flex-shrink-0"></i>
                  <div class="flex-1">
                    <div class="flex items-center justify-between">
                      <span class="font-bold"></span>
                      <span class="text-[9px] px-1.5 py-0.5 rounded uppercase font-bold "></span>
                    </div>
                    <p class="opacity-80 text-[11px] mt-0.5"></p>
                  </div>
                </div>;
            });
            
            document.getElementById('eb-flags-count').textContent = triggerCount + ' Cảnh báo kích hoạt';
            if (triggerCount > 0) {
                document.getElementById('eb-flags-count').className = 'text-[10px] px-2 py-0.5 rounded-full bg-[#FEF3F2] text-[#B42318] border border-[#FECDCA] font-semibold';
            } else {
                document.getElementById('eb-flags-count').className = 'text-[10px] px-2 py-0.5 rounded-full bg-[#ECFDF3] text-[#027A48] border border-[#A6F4C5] font-semibold';
            }
            
            showToast('Thẩm định AI thành công');
            
        } catch (err) {
            showToast('Lỗi thẩm định AI: ' + err.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    }
'''

import re
content = re.sub(r'async function runEBAssessment\(\) \{.*?(?=async function exportDocxMemo)', new_run + '\n    ', content, flags=re.DOTALL)

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated runEBAssessment")
