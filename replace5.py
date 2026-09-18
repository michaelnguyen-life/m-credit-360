# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

payload_helper = '''
    function buildEBPayload() {
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
'''

# 1. Inject buildEBPayload before runEBAssessment
content = content.replace("async function runEBAssessment() {", payload_helper + "\n    async function runEBAssessment() {")

# 2. Fix runEBAssessment body
old_runEB_try = r"try \{\s*const taxId = document\.getElementById\('eb-tax-id'\)\.value;.*?const res = await fetch\('/assess',"
new_runEB_try = '''try {
            const taxId = document.getElementById('eb-tax-id').value;
            if (!taxId) {
                showToast('Lỗi: Cần nhập Mã số thuế trước khi thẩm định', 'error');
                return;
            }
            const payload = buildEBPayload();
            const res = await fetch('/assess', '''
content = re.sub(old_runEB_try, new_runEB_try, content, flags=re.DOTALL)

# 3. Fix exportDocxMemo body
old_export_try = r"try \{\s*const taxId = document\.getElementById\('eb-tax-id'\)\.value \|\| \"mock\";.*?const res = await fetch\('/build-memo-docx',"
new_export_try = '''try {
            const payload = buildEBPayload();
            const res = await fetch('/build-memo-docx', '''
content = re.sub(old_export_try, new_export_try, content, flags=re.DOTALL)

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
print("REPLACED FUNCTIONS")
