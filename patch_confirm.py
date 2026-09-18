# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('templates/index.html', 'r', 'utf-8').read()

target = '''// Generate new Session ID
      const newSessionId = "MSB-EB-2026-" + Math.floor(100 + Math.random() * 900);
      document.getElementById('session-id-display').textContent = newSessionId;'''

replacement = '''// Generate new Session ID
      const newSessionId = "MSB-EB-2026-" + Math.floor(100 + Math.random() * 900);
      document.getElementById('session-id-display').textContent = newSessionId;
      
      // Auto-populate if preloaded
      if (window.preloadedCustomer && window.preloadedCustomer.financials) {
          const f = window.preloadedCustomer.financials;
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
          
          currentUploadedFileName = window.preloadedCustomer.filename || "BCTC_Saved.pdf";
          const sourceTag = document.getElementById('eb-source-tag');
          if (sourceTag) sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đã tải từ DB)";
          document.getElementById('eb-empty-state')?.classList.add('hidden');
          document.getElementById('eb-results-container')?.classList.remove('hidden');
      }'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('templates/index.html', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
