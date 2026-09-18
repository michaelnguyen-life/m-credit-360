# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

# 1. Add 'Lưu hồ sơ' button
btn_target = '''<button onclick="exportDocxMemo()" id="btn-export-docx" class="px-3.5 py-2 rounded-lg bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition">'''
btn_replacement = '''<button onclick="saveCustomerProfile()" id="btn-save-profile" class="px-4 py-2 rounded-lg bg-yellow-500 hover:bg-yellow-600 text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="save" class="w-3.5 h-3.5"></i>
            <span>LƯU HỒ SƠ</span>
          </button>
          <button onclick="exportDocxMemo()" id="btn-export-docx" class="px-3.5 py-2 rounded-lg bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition">'''
if btn_target in content:
    content = content.replace(btn_target, btn_replacement)
    print("Added Save Button")

# 2. Add the JS function for saveCustomerProfile
js_target = '''function openNewCustomerModal() {'''
js_replacement = '''
    async function saveCustomerProfile() {
        const mst = document.getElementById('eb-tax-id').value.trim();
        const name = document.getElementById('eb-company-name').value.trim();
        if (!mst) {
            showToast('Vui lòng nhập Mã số thuế trước khi lưu!', 'error');
            return;
        }
        
        // Collect financials if any
        const f = window.pendingEBData && window.pendingEBData.financials ? window.pendingEBData.financials : {};
        // If window.pendingEBData is null but inputs have values, parse them?
        // Let's just use what's on screen if we want
        const parseVal = (id) => {
            const val = document.getElementById(id).value.replace(/[^0-9-]/g, '');
            return val ? parseInt(val) : 0;
        };
        const currentFinancials = {
            IS_REVENUE: parseVal('eb-revenue'),
            IS_EBIT: parseVal('eb-ebit'),
            BS_CURRENT_ASSETS: parseVal('eb-ca'),
            BS_CURRENT_LIABILITIES: parseVal('eb-cl'),
            BS_TRADE_RECEIVABLES: parseVal('eb-ar'),
            BS_INVENTORY: parseVal('eb-inv'),
            BS_TRADE_PAYABLES: parseVal('eb-ap'),
            BS_EQUITY: parseVal('eb-equity'),
            IS_INTEREST_EXPENSE: parseVal('eb-interest')
        };
        
        const payload = {
            mst: mst,
            name: name,
            financials: Object.keys(f).length > 0 ? f : currentFinancials,
            filename: currentUploadedFileName || 'BCTC_KhachHang.pdf'
        };
        
        try {
            const res = await fetch('/api/customer/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.success) {
                showToast('Đã lưu hồ sơ khách hàng thành công!', 'success');
            } else {
                showToast('Lỗi khi lưu hồ sơ', 'error');
            }
        } catch(e) {
            showToast('Lỗi mạng khi lưu', 'error');
        }
    }

    function openNewCustomerModal() {'''
if js_target in content:
    content = content.replace(js_target, js_replacement)
    print("Added saveCustomerProfile JS")

# 3. Modify mockModalLookup to fetch customer data
modal_lookup_target = '''async function mockModalLookup() {
        const mst = document.getElementById('modal-tax-id').value.trim();
        const nameInput = document.getElementById('modal-company-name');
        if(!mst) { showToast('Vui lòng nhập MST hoặc CCCD trước khi tra cứu', 'error'); return; }
        showToast('Đang tra cứu dữ liệu quốc gia...', 'info');
        try {
            const res = await fetch('/api/lookup-mst?mst=' + mst);
            const data = await res.json();
            if (data.success && data.name) {
                nameInput.value = data.name;
                showToast('Tra cứu thành công!', 'info');
            } else {
                showToast('Không tìm thấy doanh nghiệp (API)', 'warning');
            }
        } catch(e) {
            showToast('Lỗi tra cứu', 'error');
        }
    }'''
    
modal_lookup_rep = '''async function mockModalLookup() {
        const mst = document.getElementById('modal-tax-id').value.trim();
        const nameInput = document.getElementById('modal-company-name');
        if(!mst) { showToast('Vui lòng nhập MST hoặc CCCD trước khi tra cứu', 'error'); return; }
        showToast('Đang tra cứu dữ liệu quốc gia...', 'info');
        try {
            // First try to load from local saved DB
            const loadRes = await fetch('/api/customer/load?mst=' + mst);
            const loadData = await loadRes.json();
            if (loadData.success && loadData.data) {
                nameInput.value = loadData.data.name;
                window.preloadedCustomer = loadData.data;
                showToast('Đã tìm thấy hồ sơ lưu trữ!', 'success');
                return;
            }
            window.preloadedCustomer = null;
            
            const res = await fetch('/api/lookup-mst?mst=' + mst);
            const data = await res.json();
            if (data.success && data.name) {
                nameInput.value = data.name;
                showToast('Tra cứu thành công!', 'info');
            } else {
                showToast('Không tìm thấy doanh nghiệp (API)', 'warning');
            }
        } catch(e) {
            showToast('Lỗi tra cứu', 'error');
        }
    }'''
if modal_lookup_target in content:
    content = content.replace(modal_lookup_target, modal_lookup_rep)
    print("Modified mockModalLookup JS")

# 4. Modify mockMSTLookup to fetch customer data
mst_lookup_target = '''async function mockMSTLookup() {
        const mst = document.getElementById('eb-tax-id').value.trim();
        const nameInput = document.getElementById('eb-company-name');
        if(!mst) { showToast('Vui lòng nhập MST trước khi tra cứu', 'error'); return; }
        showToast('Đang tra cứu cơ sở dữ liệu quốc gia...', 'info');
        try {
            const res = await fetch('/api/lookup-mst?mst=' + mst);
            const data = await res.json();
            if (data.success && data.name) {
                nameInput.value = data.name;
                showToast('Tra cứu thành công!', 'info');
            } else {
                showToast('Không tìm thấy doanh nghiệp (API)', 'warning');
            }
        } catch(e) {
            showToast('Lỗi tra cứu', 'error');
        }
    }'''

mst_lookup_rep = '''async function mockMSTLookup() {
        const mst = document.getElementById('eb-tax-id').value.trim();
        const nameInput = document.getElementById('eb-company-name');
        if(!mst) { showToast('Vui lòng nhập MST trước khi tra cứu', 'error'); return; }
        showToast('Đang tra cứu cơ sở dữ liệu quốc gia...', 'info');
        try {
            const loadRes = await fetch('/api/customer/load?mst=' + mst);
            const loadData = await loadRes.json();
            if (loadData.success && loadData.data) {
                nameInput.value = loadData.data.name;
                
                // Restore financials
                const f = loadData.data.financials;
                if (f && Object.keys(f).length > 0) {
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
                    window.pendingEBData = { financials: f };
                    
                    const sourceTag = document.getElementById('eb-source-tag');
                    currentUploadedFileName = loadData.data.filename || "BCTC_Saved.pdf";
                    if (sourceTag) sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đã tải từ DB)";
                    document.getElementById('eb-empty-state')?.classList.add('hidden');
                    document.getElementById('eb-results-container')?.classList.remove('hidden');
                }
                
                showToast('Đã tìm thấy hồ sơ lưu trữ!', 'success');
                return;
            }
            
            const res = await fetch('/api/lookup-mst?mst=' + mst);
            const data = await res.json();
            if (data.success && data.name) {
                nameInput.value = data.name;
                showToast('Tra cứu thành công!', 'info');
            } else {
                showToast('Không tìm thấy doanh nghiệp (API)', 'warning');
            }
        } catch(e) {
            showToast('Lỗi tra cứu', 'error');
        }
    }'''

if mst_lookup_target in content:
    content = content.replace(mst_lookup_target, mst_lookup_rep)
    print("Modified mockMSTLookup JS")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
