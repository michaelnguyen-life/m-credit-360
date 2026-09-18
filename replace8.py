# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index_backup.html', 'r', 'utf-8').read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# 1. FIX: handleFileSelect fallback removal and normalized_financials
target1 = '''            if (result.status === 'success' && result.data && result.data.financials) {
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

replacement1 = '''            if (result.status === 'success' && result.data && result.data.normalized_financials) {
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

if target1 in content:
    content = content.replace(target1, replacement1)
    print("Fixed handleFileSelect fallback")
else:
    print("COULD NOT FIND TARGET1")

# 2. Add buildEBPayload before runEBAssessment
target2 = '''    async function runEBAssessment() {'''

replacement2 = '''    function buildEBPayload() {
        const taxId = document.getElementById('eb-tax-id').value || "mock";
        const parseNum = (id) => {
            const el = document.getElementById(id);
            if (!el || !el.value) return null;
            const v = el.value.replace(/[^0-9-]/g, '');
            return v ? parseFloat(v) : null;
        };
        return {
            assessment_id: "EB-" + Date.now(),
            company: {
                tax_id: taxId,
                name: document.getElementById('eb-company-name').value
            },
            financials: {
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
            dsp: window.pendingEBData?.dsp || {},
            product_039: {
                ...(window.pendingEBData?.product_039 || {}),
                contract_value: parseNum('eb-p039-contract'),
                loan_request_amount: parseNum('eb-p039-loan'),
                customer_equity: parseNum('eb-equity')
            }
        };
    }

    async function runEBAssessment() {'''
if target2 in content:
    content = content.replace(target2, replacement2)
    print("Added buildEBPayload")
else:
    print("COULD NOT FIND TARGET2")

# 3. Replace runEBAssessment body
target3 = '''        try {
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
                dsp: window.pendingEBData?.dsp || {},
                product_039: {
                    ...(window.pendingEBData?.product_039 || {}),
                    contract_value: parseNum('eb-p039-contract'),
                    loan_request_amount: parseNum('eb-p039-loan'),
                    customer_equity: parseNum('eb-equity')
                }
            };

            const res = await fetch('/assess', {'''

replacement3 = '''        try {
            const taxId = document.getElementById('eb-tax-id').value;
            if (!taxId) {
                showToast('Lỗi: Cần nhập Mã số thuế trước khi thẩm định', 'error');
                return;
            }
            
            const payload = buildEBPayload();
            const res = await fetch('/assess', {'''

if target3 in content:
    content = content.replace(target3, replacement3)
    print("Replaced runEBAssessment body")
else:
    print("COULD NOT FIND TARGET3")

# 4. Replace exportDocxMemo body
target4 = '''        try {
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

            const res = await fetch('/build-memo-docx', {'''

replacement4 = '''        try {
            const payload = buildEBPayload();
            const res = await fetch('/build-memo-docx', {'''

if target4 in content:
    content = content.replace(target4, replacement4)
    print("Replaced exportDocxMemo body")
else:
    print("COULD NOT FIND TARGET4")

# 5. Fix taxId in exportDocxMemo download
target5 = '''            a.download = 'To_Trinh_MB02a_' + taxId + '.docx';'''
replacement5 = '''            a.download = 'To_Trinh_MB02a_' + payload.company.tax_id + '.docx';'''
if target5 in content:
    content = content.replace(target5, replacement5)
    print("Replaced taxId in download")
else:
    print("COULD NOT FIND TARGET5")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
print("ALL DONE")
