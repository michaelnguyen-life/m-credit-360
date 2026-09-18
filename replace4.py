# -*- coding: utf-8 -*-
import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

# 1. Fix handleFileSelect (remove fallback, use normalized_financials)
target_handle = '''            if (result.status === 'success' && result.data && result.data.financials) {
                // Populate inputs
                const f = result.data.financials;
                const setVal = (id, val) => { const el = document.getElementById(id); if (el && val != null) el.value = val.toLocaleString('vi-VN'); };
                setVal('eb-revenue', f.IS_REVENUE);
                setVal('eb-ebit', f.IS_EBIT);
                setVal('eb-ca', f.BS_CURRENT_ASSETS);
                setVal('eb-cl', f.BS_CURRENT_LIABILITIES);
                setVal('eb-ar', f.BS_TRADE_RECEIVABLES);
                setVal('eb-inv', f.BS_INVENTORY);
                setVal('eb-ap', f.BS_TRADE_PAYABLES);
                setVal('eb-equity', f.BS_EQUITY);
                setVal('eb-interest', f.IS_INTEREST_EXPENSE);
                
                // Save to pendingEBData
                window.pendingEBData = { financials: f };
                
                showToast('Bóc tách tài liệu PDF thành công!', 'success');
                document.getElementById('eb-empty-state')?.classList.add('hidden');
                document.getElementById('eb-results-container')?.classList.remove('hidden');
            } else {
                // Fallback to sample if upload doesn't return financials
                showToast('Không trích xuất được BCTC thực tế, dùng dữ liệu mẫu thay thế.', 'warning');
                let detectedType = 'alpha';
                const lowerName = currentUploadedFileName.toLowerCase();
                if (lowerName.includes('khang') || lowerName.includes('thinh')) detectedType = 'eb_good_1';
                else if (lowerName.includes('vinamilk') || lowerName.includes('vnm')) detectedType = 'eb_good_2';
                else if (lowerName.includes('flc')) detectedType = 'eb_bad_1';
                else if (lowerName.includes('tanhoangminh') || lowerName.includes('thm')) detectedType = 'eb_bad_2';
                openExtractionReview(detectedType);
            }'''

replacement_handle = '''            if (result.status === 'success' && result.data && result.data.normalized_financials) {
                // Populate inputs
                const f = result.data.normalized_financials;
                const setVal = (id, val) => { const el = document.getElementById(id); if (el && val != null) el.value = val.toLocaleString('vi-VN'); };
                setVal('eb-revenue', f.IS_REVENUE);
                setVal('eb-ebit', f.IS_EBIT);
                setVal('eb-ca', f.BS_CURRENT_ASSETS);
                setVal('eb-cl', f.BS_CURRENT_LIABILITIES);
                setVal('eb-ar', f.BS_TRADE_RECEIVABLES);
                setVal('eb-inv', f.BS_INVENTORY);
                setVal('eb-ap', f.BS_TRADE_PAYABLES);
                setVal('eb-equity', f.BS_EQUITY);
                setVal('eb-interest', f.IS_INTEREST_EXPENSE);
                
                // Save to pendingEBData
                window.pendingEBData = { financials: f };
                
                showToast('Bóc tách tài liệu PDF thành công!', 'success');
                document.getElementById('eb-empty-state')?.classList.add('hidden');
                document.getElementById('eb-results-container')?.classList.remove('hidden');
            } else {
                showToast('Không trích xuất được BCTC thực tế: ' + (result.message || 'Thiếu dữ liệu normalized_financials'), 'error');
            }'''

# Note: The existing file has Vietnamese accents in the code block. 
# It might fail exactly matching. Let's just use regex for handleFileSelect.

import re
content = re.sub(r"if \(result\.status === 'success' && result\.data && result\.data\.financials\).*?openExtractionReview\(detectedType\);\s*}", replacement_handle, content, flags=re.DOTALL)


# 2. Fix exportDocxMemo payload
target_export = '''                financials: {
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
                }'''

replacement_export = '''                financials: {
                    ...(window.pendingEBData?.financials || {}),
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
                    ...(window.pendingEBData?.debt_service || {}),
                    principal_due: parseNum('eb-principal')
                },
                product_039: {
                    ...(window.pendingEBData?.product_039 || {}),
                    contract_value: parseNum('eb-p039-contract'),
                    loan_request_amount: parseNum('eb-p039-loan'),
                    customer_equity: parseNum('eb-equity')
                }'''

content = content.replace(target_export, replacement_export)

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
print("INDEX FIXED")
