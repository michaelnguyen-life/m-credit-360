# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target1 = '''function mockModalLookup() {
        const mst = document.getElementById('modal-tax-id').value.trim();
        const nameInput = document.getElementById('modal-company-name');
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
    }'''

rep1 = '''async function mockModalLookup() {
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

target2 = '''function mockMSTLookup() {
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
    }'''

rep2 = '''async function mockMSTLookup() {
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

if target1 in content:
    content = content.replace(target1, rep1)
    print("SUCCESS 1")
else:
    print("FAILED 1")

if target2 in content:
    content = content.replace(target2, rep2)
    print("SUCCESS 2")
else:
    print("FAILED 2")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
