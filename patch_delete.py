# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

# Modify handleFileSelect to add the file to the list with a delete button
target = '''window.pendingEBData = { financials: f };
                  
                  showToast('Bóc tách thành công!', 'success');
                  document.getElementById('eb-empty-state')?.classList.add('hidden');
                  document.getElementById('eb-results-container')?.classList.remove('hidden');'''

replacement = '''window.pendingEBData = { financials: f };
                  
                  showToast('Bóc tách thành công!', 'success');
                  document.getElementById('eb-empty-state')?.classList.add('hidden');
                  document.getElementById('eb-results-container')?.classList.remove('hidden');
                  
                  // Add file to sidebar list
                  const fileList = document.getElementById('file-ingested-list');
                  if (fileList) {
                      const fileId = "file-" + Date.now();
                      const fileHTML = \
                      <div id="\" class="flex items-center justify-between p-2 rounded bg-white border border-[#EAECF0] hover:border-[#FF5A00] transition">
                        <div class="flex items-center gap-2 overflow-hidden">
                            <i data-lucide="file-text" class="w-4 h-4 text-[#FF5A00] shrink-0"></i>
                            <span class="text-xs text-[#344054] truncate" title="\">\</span>
                        </div>
                        <button onclick="deleteUploadedFile('\')" class="text-gray-400 hover:text-red-500 transition" title="Xóa tài liệu">
                            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                        </button>
                      </div>\;
                      fileList.innerHTML = fileHTML; // Replace list with this single file for simplicity, or append.
                      if (typeof lucide !== 'undefined') lucide.createIcons();
                  }
                  const allFilesLink = document.querySelector('a[href="#all-files"]');
                  if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (1)';'''

if target in content:
    content = content.replace(target, replacement)
    print("SUCCESS handleFileSelect")
else:
    print("FAILED handleFileSelect")

# Add the delete function
target_js = '''function openNewCustomerModal() {'''
replacement_js = '''
    function deleteUploadedFile(fileId) {
        // Remove from UI
        const fileEl = document.getElementById(fileId);
        if (fileEl) fileEl.remove();
        
        // Reset counters
        const allFilesLink = document.querySelector('a[href="#all-files"]');
        if (allFilesLink) allFilesLink.textContent = 'Xem tất cả (0)';
        
        // Clear data
        currentUploadedFileName = "";
        window.pendingEBData = null;
        
        // Clear form fields
        const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
        setVal('eb-revenue', '0');
        setVal('eb-ebit', '0');
        setVal('eb-ca', '0');
        setVal('eb-cl', '0');
        setVal('eb-ar', '0');
        setVal('eb-inv', '0');
        setVal('eb-ap', '0');
        setVal('eb-equity', '0');
        setVal('eb-interest', '0');
        
        // Revert UI states
        const sourceTag = document.getElementById('eb-source-tag');
        if (sourceTag) sourceTag.textContent = "Nguồn: Chưa có dữ liệu";
        document.getElementById('eb-empty-state')?.classList.remove('hidden');
        document.getElementById('eb-results-container')?.classList.add('hidden');
        
        showToast('Đã xóa tài liệu', 'info');
    }

    function openNewCustomerModal() {'''

if target_js in content:
    content = content.replace(target_js, replacement_js)
    print("SUCCESS deleteUploadedFile")
else:
    print("FAILED deleteUploadedFile")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
