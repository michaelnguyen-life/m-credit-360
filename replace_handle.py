# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

new_handle = '''function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      const file = files[0];
      currentUploadedFileName = file.name || "BCTC_Uploaded.pdf";

      const sourceTag = document.getElementById('eb-source-tag');
      if (sourceTag) {
        sourceTag.textContent = "Ngu"n: " + currentUploadedFileName + " (?ang bA3c tAch AI)";
      }

      const modal = document.getElementById('ai-processing-modal');
      const modalFilename = document.getElementById('ai-modal-filename');
      const modalBar = document.getElementById('ai-modal-bar');
      const modalPct = document.getElementById('ai-modal-pct');
      const modalStage = document.getElementById('ai-modal-stage');

      if (modalFilename) modalFilename.textContent = currentUploadedFileName;
      if (modal) modal.classList.remove('hidden');
      if (modalBar) modalBar.style.width = '30%';
      if (modalPct) modalPct.textContent = '30%';
      if (modalStage) modalStage.textContent = '?ang upload & phAn tA-ch...';
      if (typeof lucide !== 'undefined') lucide.createIcons();

      const formData = new FormData();
      formData.append('file', file);

      fetch('/api/upload', {
          method: 'POST',
          body: formData
      })
      .then(res => res.json())
      .then(result => {
          if (modalBar) modalBar.style.width = '100%';
          if (modalPct) modalPct.textContent = '100%';
          if (modalStage) modalStage.textContent = 'HoAn tt!';
          
          setTimeout(() => {
              if (modal) modal.classList.add('hidden');
              closeUploadDrawer();
              
              if (result.status === 'success' && result.data && result.data.normalized_financials) {
                  if (sourceTag) sourceTag.textContent = "Ngu"n: " + currentUploadedFileName + " (?A bA3c tAch AI)";
                  
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
                  
                  window.pendingEBData = { financials: f };
                  
                  showToast('bóc tách thành công!', 'success');
                  document.getElementById('eb-empty-state')?.classList.add('hidden');
                  document.getElementById('eb-results-container')?.classList.remove('hidden');
              } else {
                  if (sourceTag) sourceTag.textContent = "Ngu"n: " + currentUploadedFileName + " (L-i bA3c tAch)";
                  showToast('Lỗi: ' + (result.message || 'Thiếu dữ liệu normalized_financials'), 'error');
              }
          }, 500);
      })
      .catch(err => {
          if (modal) modal.classList.add('hidden');
          if (sourceTag) sourceTag.textContent = "Ngu"n: " + currentUploadedFileName + " (L-i mng)";
          showToast('Lỗi upload: ' + err.message, 'error');
      });
    }'''

old_handle = re.search(r"function handleFileSelect\(e\) \{.*?openExtractionReview\(detectedType\);\s*\}\s*\}, 600\);\s*\}\s*\}, 400\);\s*\}", content, flags=re.DOTALL)
if old_handle:
    content = content.replace(old_handle.group(0), new_handle)
    print("Replaced handleFileSelect")
else:
    print("Could not find handleFileSelect")

codecs.open('templates/index.html', 'w', 'utf-8').write(content)
