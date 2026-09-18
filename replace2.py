# -*- coding: utf-8 -*-
import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

code = '''
    async function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      const file = files[0];
      currentUploadedFileName = file.name || "BCTC_Uploaded.pdf";

      const sourceTag = document.getElementById('eb-source-tag');
      if (sourceTag) {
        sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đang bóc tách AI)";
      }

      const box = document.getElementById('ai-processing-box');
      if (box) box.classList.remove('hidden');

      const modal = document.getElementById('ai-processing-modal');
      const modalFilename = document.getElementById('ai-modal-filename');
      const modalBar = document.getElementById('ai-modal-bar');
      const modalPct = document.getElementById('ai-modal-pct');
      const modalStage = document.getElementById('ai-modal-stage');

      if (modalFilename) modalFilename.textContent = currentUploadedFileName;
      if (modal) modal.classList.remove('hidden');
      if (typeof lucide !== 'undefined') lucide.createIcons();

      const updateProgress = (pct, stage) => {
        if (modalBar) modalBar.style.width = pct + '%';
        if (modalPct) modalPct.textContent = pct + '%';
        if (modalStage) modalStage.textContent = stage;
        const bar = document.getElementById('ai-stage-bar');
        const pctText = document.getElementById('ai-stage-pct');
        const stageText = document.getElementById('ai-stage-text');
        if (bar) bar.style.width = pct + '%';
        if (pctText) pctText.textContent = pct + '%';
        if (stageText) stageText.textContent = stage;
      };

      updateProgress(15, "Giai đoạn 1/6: Đang tải lên...");
      
      const formData = new FormData();
      formData.append('file', file);
      
      try {
          updateProgress(45, "Giai đoạn 3/6: AI OCR bóc tách BCTC...");
          const res = await fetch('/api/upload', {
              method: 'POST',
              body: formData
          });
          updateProgress(85, "Giai đoạn 5/6: Xử lý số liệu tài chính...");
          const result = await res.json();
          updateProgress(100, "Giai đoạn 6/6: Hoàn tất bóc tách dữ liệu!");
          
          setTimeout(() => {
            if (modal) modal.classList.add('hidden');
            closeUploadDrawer();
            if (sourceTag) sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đã bóc tách AI)";
            
            if (result.status === 'success' && result.data && result.data.financials) {
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
            }
          }, 500);
      } catch (err) {
          showToast('Lỗi khi tải file lên: ' + err.message, 'error');
          if (modal) modal.classList.add('hidden');
      }
    }
'''

start = content.find('function handleFileSelect(e)')
end = content.find('function openExtractionReview(type)', start)
if start != -1 and end != -1:
    end = content.rfind('// 5. Data Extraction Review Modal Logic', start, end)
    new_content = content[:start] + code + '\n\n    ' + content[end:]
    codecs.open('templates/index.html', 'w', 'utf-8').write(new_content)
    print("REPLACED")
else:
    print("NOT FOUND", start, end)
