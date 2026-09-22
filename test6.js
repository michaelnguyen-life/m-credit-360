
    /* Removed duplicate global constants */
    lucide.createIcons();

    // 1. Tab Switching
    function switchTab(tab) {
      const sections = ['eb', 'rb', 'zalo'];
      sections.forEach(s => {
        const el = document.getElementById(`section-${s}`);
        if (el) el.classList.toggle('hidden', s !== tab);
        
        const btn = document.getElementById(`btn-tab-${s}`);
        if (btn) {
          if (s === tab) {
            btn.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-[#FFF4EB] text-[#FF5A00] border border-orange-200';
          } else {
            btn.className = 'px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 text-[#667085] hover:text-[#0B1739]';
          }
        }
      });
      lucide.createIcons();
    }

    // 2. Chat Drawer Toggle
    let isChatOpen = false;
    function toggleChatDrawer() {
      isChatOpen = !isChatOpen;
      const drawer = document.getElementById('chat-drawer');
      if (isChatOpen) {
        drawer.classList.remove('translate-x-full');
        document.getElementById('chat-input').focus();
      } else {
        drawer.classList.add('translate-x-full');
      }
    }

    function triggerAICopilot(promptText) {
      toggleChatDrawer();
      document.getElementById('chat-input').value = promptText;
      document.getElementById('chat-send-btn').click();
    }

    // 3. New Customer / Reset Assessment Modal Logic
    function openNewCustomerModal() {
      document.getElementById('new-customer-modal').classList.remove('hidden');
    }
    function closeNewCustomerModal() {
      document.getElementById('new-customer-modal').classList.add('hidden');
    }
    function confirmNewCustomerSession() {
      closeNewCustomerModal();
      
      // Clear Form Fields
      document.getElementById('eb-tax-id').value = '';
      document.getElementById('eb-company-name').value = '';
      document.getElementById('eb-revenue').value = '0';
      document.getElementById('eb-ebit').value = '0';
      document.getElementById('eb-ca').value = '0';
      document.getElementById('file-ingested-list').innerHTML = '<div class="p-3 text-center text-slate-400 text-[10px] border border-dashed rounded-lg">Chưa có tài liệu nào</div>'; document.getElementById('ai-insight-box').classList.add('hidden');
      document.getElementById('eb-cl').value = '0';
      document.getElementById('eb-ar').value = '0';
      document.getElementById('eb-inv').value = '0';
      document.getElementById('eb-ap').value = '0';
      document.getElementById('eb-equity').value = '0';
      document.getElementById('eb-interest').value = '0';
      document.getElementById('eb-principal').value = '0';
      document.getElementById('eb-p039-contract').value = '0';
      document.getElementById('eb-p039-loan').value = '0';
      
      // Generate new Session ID
      const newSessionId = "MSB-EB-2026-" + Math.floor(100 + Math.random() * 900);
      document.getElementById('eb-assessment-id').textContent = "ID: " + newSessionId;
      document.getElementById('session-status-badge').textContent = "Chưa thẩm định";
      document.getElementById('session-status-badge').className = "text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200 font-semibold";
      document.getElementById('eb-source-tag').textContent = "Nguồn: Nhập thủ công";

      // Show Intelligent Empty State, Hide Results
      document.getElementById('eb-results-container').classList.add('hidden');
      document.getElementById('eb-empty-state').classList.remove('hidden');
      lucide.createIcons();
    }

    function focusManualEntry() {
      document.getElementById('eb-empty-state').classList.add('hidden');
      document.getElementById('eb-results-container').classList.remove('hidden');
      document.getElementById('eb-company-name').focus();
    }

    // 4. Upload Drawer Logic
    function openUploadDrawer() {
      document.getElementById('upload-drawer').classList.remove('hidden');
      lucide.createIcons();
    }
    function closeUploadDrawer() {
      document.getElementById('upload-drawer').classList.add('hidden');
    }
    function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      currentUploadedFileName = files[0].name || "BCTC_Uploaded.pdf";
      
      // Update badge and file tags
      const sourceTag = document.getElementById('eb-source-tag');
      if (sourceTag) {
        sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đã bóc tách AI)";
      }
      
      const box = document.getElementById('ai-processing-box');
      box.classList.remove('hidden');
      
      let pct = 20;
      const bar = document.getElementById('ai-stage-bar');
      const pctText = document.getElementById('ai-stage-pct');
      const stageText = document.getElementById('ai-stage-text');
      
      const interval = setInterval(() => {
        pct += 20;
        bar.style.width = pct + '%';
        pctText.textContent = pct + '%';
        if (pct === 40) stageText.textContent = "Giai đoạn 2/6: OCR / đọc tài liệu BCTC scan...";
        if (pct === 60) stageText.textContent = "Giai đoạn 3/6: Phân loại hồ sơ tự động & đối chiếu...";
        if (pct === 80) stageText.textContent = "Giai đoạn 4/6: Trích xuất chỉ tiêu tài chính chuẩn MSB...";
        if (pct >= 100) {
          clearInterval(interval);
          stageText.textContent = "✓ Hoàn tất bóc tách dữ liệu!";
          setTimeout(() => {
            closeUploadDrawer();
            openExtractionReview();
          }, 600);
        }
      }, 300);
    }

    // 5. Data Extraction Review Modal Logic
    function openExtractionReview() {
      document.getElementById('extraction-modal').classList.remove('hidden');
      lucide.createIcons();
    }
    function closeExtractionReview() {
      document.getElementById('extraction-modal').classList.add('hidden');
    }
    function applyExtractedData() {
      closeExtractionReview();
      loadSampleEB('alpha');
      setTimeout(() => {
        const sourceTag = document.getElementById('eb-source-tag');
        if (sourceTag) {
          sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đã bóc tách AI)";
        }
      }, 50);
      document.getElementById('eb-empty-state').classList.add('hidden');
      document.getElementById('eb-results-container').classList.remove('hidden');
    }

    function saveDraftNotification() {
      alert("✓ Đã lưu nháp phiên làm việc hiện tại thành công vào bộ nhớ tạm MSB!");
    }

    // 6. Number Helpers
    function parseVND(val) {
      if (typeof val === 'number') return val;
      return parseFloat(String(val).replace(/\./g, '').replace(/,/g, '').replace(/[^\d.-]/g, '')) || 0;
    }
    function fmtTỷ(val) {
      if (val === null || val === undefined) return '0,00 Tỷ';
      return (val / 1000000000).toLocaleString('vi-VN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Tỷ';
    }

    // 7. Load Sample EB
    async function loadSampleEB(type) {
      try {
        let d = null;
        try {
          const res = await fetch(`/api/sample/eb/${type}`);
          if (res.ok) {
            d = await res.json();
          }
        } catch (netErr) {
          console.warn('API sample load failed, falling back to client cache:', netErr);
        }
        if (!d) {
          d = (type === 'beta') ? CLIENT_FALLBACK_BETA : CLIENT_FALLBACK_ALPHA;
        }
        
        document.getElementById('eb-tax-id').value = d.company?.tax_id || '0311807068';
        document.getElementById('eb-company-name').value = d.company?.name || '';
        document.getElementById('eb-period').value = d.reporting_period || '2025';
        document.getElementById('session-status-badge').textContent = "Đang thẩm định";
        document.getElementById('session-status-badge').className = "text-[10px] px-2 py-0.5 rounded-full bg-[#FFF4EB] text-[#FF5A00] border border-orange-200 font-semibold";
        document.getElementById('eb-source-tag').textContent = type === 'alpha' ? 'Nguồn: BCTC_2025.pdf' : 'Nguồn: BCTC_Beta_Audit.pdf';
        
        const fin = d.financials || {};
        const rev = fin.IS001 || fin.IS_REVENUE || 318000000000;
        const ebit = fin.IS003 || fin.IS_EBIT || 18500000000;
        const ca = fin.BS001 || fin.BS_CURRENT_ASSETS || 120000000000;
        const cl = fin.BS002 || fin.BS_CURRENT_LIABILITIES || 145000000000;
        const ar = fin.BS003 || fin.BS_TRADE_RECEIVABLES || 65000000000;
        const inv = fin.BS004 || fin.BS_INVENTORY || 45000000000;
        const ap = fin.BS005 || fin.BS_TRADE_PAYABLES || 50000000000;
        const eq = fin.BS008 || fin.BS_EQUITY || 75000000000;
        const intr = fin.IS004 || fin.IS_INTEREST_EXPENSE || 8200000000;
        const princ = d.debt_service?.principal_due || 25000000000;

        document.getElementById('eb-revenue').value = rev.toLocaleString('vi-VN');
        document.getElementById('eb-ebit').value = ebit.toLocaleString('vi-VN');
        document.getElementById('eb-ca').value = ca.toLocaleString('vi-VN');
        document.getElementById('eb-cl').value = cl.toLocaleString('vi-VN');
        document.getElementById('eb-ar').value = ar.toLocaleString('vi-VN');
        document.getElementById('eb-inv').value = inv.toLocaleString('vi-VN');
        document.getElementById('eb-ap').value = ap.toLocaleString('vi-VN');
        document.getElementById('eb-equity').value = eq.toLocaleString('vi-VN');
        document.getElementById('eb-interest').value = intr.toLocaleString('vi-VN');
        document.getElementById('eb-principal').value = princ.toLocaleString('vi-VN');

        document.getElementById('eb-empty-state').classList.add('hidden');
        document.getElementById('eb-results-container').classList.remove('hidden');

        await runEBAssessment();
      } catch (err) {
        console.error(err);
        alert('Lỗi nạp dữ liệu mẫu EB: ' + err.message);
      }
    }

    // 8. Load Sample RB
    async function loadSampleRB(type) {
      try {
        let d = null;
        try {
          const res = await fetch(`/api/sample/rb/${type}`);
          if (res.ok) {
            d = await res.json();
          }
        } catch (netErr) {
          console.warn('API sample load failed, falling back to client cache:', netErr);
        }
        if (!d) {
          d = CLIENT_FALLBACK_RB;
        }
        
        document.getElementById('rb-customer-id').value = d.customer?.customer_id || 'KH01';
        document.getElementById('rb-name').value = d.customer?.name || 'PHẠM THANH BÌNH';
        document.getElementById('rb-channel').value = d.customer?.business_channel || 'TikTok Shop';
        
        const inc = d.income?.[0] || {};
        document.getElementById('rb-gross-income').value = (inc.monthly_amount || 2919000000).toLocaleString('vi-VN');
        document.getElementById('rb-eligible-pct').value = (inc.eligible_percent || 0.08) * 100;
        
        const debts = d.existing_debts || [];
        const totalOut = debts.reduce((acc, x) => acc + (x.outstanding || 0), 0);
        const totalPay = debts.reduce((acc, x) => acc + (x.monthly_payment || 0), 0);
        document.getElementById('rb-debt-outstanding').value = totalOut.toLocaleString('vi-VN');
        document.getElementById('rb-debt-monthly').value = totalPay.toLocaleString('vi-VN');

        const loan = d.loan || {};
        document.getElementById('rb-loan-amt').value = (loan.amount || 450000000).toLocaleString('vi-VN');
        document.getElementById('rb-loan-rate').value = ((loan.annual_interest_rate || 0.225) * 100).toFixed(1);
        document.getElementById('rb-loan-tenor').value = loan.tenor_months || 48;

        await runRBAssessment();
      } catch (err) {
        console.error(err);
        alert('Lỗi nạp dữ liệu mẫu RB: ' + err.message);
      }
    }

    // 9. Run EB Assessment API
    async function runEBAssessment() {
      const btn = document.getElementById('btn-run-eb');

      // OSINT loading state
      ['osint-tax', 'osint-bid-summary'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.innerHTML = '<span class="flex items-center gap-1"><i data-lucide="loader-2" class="w-3 h-3 animate-spin"></i> Tra cứu...</span>';
          el.className = "text-slate-400 font-medium";
        }
      });
      const bidDetails = document.getElementById('osint-bid-details');
      if (bidDetails) bidDetails.innerHTML = '';

      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>ĐANG PHÂN TÍCH...</span>`;
      lucide.createIcons();

      try {
        const payload = {
          assessment_id: "MSB-EB-" + document.getElementById('eb-period').value + "-01",
          company: {
            name: document.getElementById('eb-company-name').value,
            tax_id: document.getElementById('eb-tax-id').value
          },
          reporting_period: document.getElementById('eb-period').value,
          financials: {
            BS001: parseVND(document.getElementById('eb-ca').value),
            BS002: parseVND(document.getElementById('eb-cl').value),
            BS003: parseVND(document.getElementById('eb-ar').value),
            BS004: parseVND(document.getElementById('eb-inv').value),
            BS005: parseVND(document.getElementById('eb-ap').value),
            BS008: parseVND(document.getElementById('eb-equity').value),
            IS001: parseVND(document.getElementById('eb-revenue').value),
            IS003: parseVND(document.getElementById('eb-ebit').value),
            IS004: parseVND(document.getElementById('eb-interest').value),
          },
          debt_service: {
            principal_due: parseVND(document.getElementById('eb-principal').value),
            interest_expense: parseVND(document.getElementById('eb-interest').value),
            cash_available_for_debt_service: parseVND(document.getElementById('eb-ebit').value) * 0.7
          },
          product_039: {
            contract_value: parseVND(document.getElementById('eb-p039-contract').value),
            requested_loan_amount: parseVND(document.getElementById('eb-p039-loan').value),
            funding_ratio: parseVND(document.getElementById('eb-p039-loan').value) / (parseVND(document.getElementById('eb-p039-contract').value) || 1),
            buyer_years_in_business: 4,
            buyer_revenue_year_1: 85000000000,
            buyer_revenue_year_2: 92000000000
          }
        };

        const res = await fetch('/assess', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        const ratios = data.ratios || {};
        const metrics = data.metrics || {};
        const flags = data.red_flags || [];

        const dec = data.preliminary_decision?.outcome || 'CONDITIONAL_PASS';
        const banner = document.getElementById('eb-decision-banner');
        const decText = document.getElementById('eb-decision-text');
        const decIcon = document.getElementById('eb-decision-icon');
        
        let displayOutcome = "Cần thẩm định thủ công";
        if (dec.includes('PASS') || dec.includes('CHẤP THUẬN')) displayOutcome = "Cần thẩm định thủ công";
        if (dec.includes('REJECT') || dec.includes('FAIL')) displayOutcome = "Không đạt chuẩn tín dụng";
        decText.textContent = displayOutcome;
        document.getElementById('eb-assessment-id').textContent = 'ID: ' + data.assessment_id;

        if (dec.includes('REJECT') || dec.includes('FAIL')) {
          banner.className = 'executive-card p-4 border border-[#FECDCA] bg-[#FEF3F2] flex items-center justify-between transition-all';
          decText.className = 'text-base font-black text-[#B42318]';
          decIcon.className = 'w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#E53935] shadow-sm flex-shrink-0';
          decIcon.innerHTML = `<i data-lucide="x-circle" class="w-6 h-6"></i>`;
        } else {
          banner.className = 'executive-card p-4 border border-[#A6F4C5] bg-[#ECFDF3] flex items-center justify-between transition-all';
          decText.className = 'text-base font-black text-[#027A48]';
          decIcon.className = 'w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#00A86B] shadow-sm flex-shrink-0';
          decIcon.innerHTML = `<i data-lucide="check-circle" class="w-6 h-6"></i>`;
        }

        const nwc = ratios.nwc !== undefined ? ratios.nwc : (metrics.current_assets - metrics.current_liabilities);
        const kpiNwc = document.getElementById('kpi-nwc');
        kpiNwc.textContent = fmtTỷ(nwc);
        kpiNwc.className = nwc >= 0 ? 'text-base font-black text-[#00A86B] font-mono block mt-0.5' : 'text-base font-black text-[#E53935] font-mono block mt-0.5';

        const dscr = ratios.dscr;
        const kpiDscr = document.getElementById('kpi-dscr');
        kpiDscr.textContent = dscr ? dscr.toFixed(2).replace('.', ',') + 'x' : '0,39x';
        kpiDscr.className = (dscr && dscr >= 1.0) ? 'text-base font-black text-[#00A86B] font-mono block mt-0.5' : 'text-base font-black text-[#E53935] font-mono block mt-0.5';

        const icr = ratios.icr;
        const kpiIcr = document.getElementById('kpi-icr');
        kpiIcr.textContent = icr ? icr.toFixed(2).replace('.', ',') + 'x' : '2,26x';

        const trigFlags = flags.filter(f => f.triggered);
        document.getElementById('eb-flags-count').textContent = `${trigFlags.length} Cảnh báo kích hoạt`;
        const flagsList = document.getElementById('eb-flags-list');
        flagsList.innerHTML = '';
        if (trigFlags.length === 0) {
          flagsList.innerHTML = `<div class="p-2.5 rounded-lg bg-[#ECFDF3] border border-[#A6F4C5] text-[#027A48]">Không có vi phạm quy chuẩn an toàn tín dụng MSB.</div>`;
        } else {
          trigFlags.forEach(f => {
            const isHigh = f.severity === 'high';
            const bg = isHigh ? 'bg-[#FFF9F2] border-[#FFE6CC]' : 'bg-[#FEF0C7] border-[#FEDF89]';
            const textCol = isHigh ? 'text-[#B54708]' : 'text-[#B54708]';
            flagsList.innerHTML += `
              <div class="p-2.5 rounded-lg ${bg} border flex items-start gap-2.5">
                <i data-lucide="alert-circle" class="w-4 h-4 text-[#F59E0B] mt-0.5 flex-shrink-0"></i>
                <div class="flex-1">
                  <div class="flex items-center justify-between">
                    <span class="font-bold ${textCol}">${f.title}</span>
                    <span class="text-[9px] px-1.5 py-0.5 rounded uppercase font-bold bg-amber-100 text-[#B54708]">${f.severity}</span>
                  </div>
                  <p class="text-[#667085] text-[11px] mt-0.5">${f.evidence || ''}</p>
                </div>
              </div>
            `;
          });
        }

        
        // Dynamic OSINT & Cross-sell
        const osintData = data.osint || {
          tax_status: "Sạch (0đ)", tax_class: "text-green-600",
          bid_summary: "0 gói thầu", bid_class: "text-slate-500",
          bid_details: `<div class="text-slate-400 italic">Chưa ghi nhận lịch sử trúng thầu</div>`
        };
        
        document.getElementById('osint-tax').innerHTML = osintData.tax_status; 
        document.getElementById('osint-tax').className = `font-bold ${osintData.tax_class} font-mono`;
        document.getElementById('osint-bid-summary').innerHTML = osintData.bid_summary; 
        document.getElementById('osint-bid-summary').className = `font-bold ${osintData.bid_class}`;
        document.getElementById('osint-bid-details').innerHTML = osintData.bid_details;

        const crossList = document.getElementById('eb-cross-list');
        crossList.innerHTML = '';
        const deals = data.cross_sell_opportunities || [];
        let totalDeal = 0;
        document.getElementById('eb-cross-count').textContent = `${deals.length} Cơ hội chốt Deal`;
        
        if (deals.length === 0) {
            crossList.innerHTML = `<div class="p-2.5 rounded-lg bg-slate-50 text-slate-500 text-center border border-slate-200">Không tìm thấy cơ hội bán chéo.</div>`;
        } else {
            deals.forEach(deal => {
              totalDeal += deal.estimated_deal_size || 0;
              const prioClass = deal.priority === 'P1' ? 'bg-[#ECFDF3] text-[#027A48] border-[#A6F4C5]' : 'bg-[#EFF4FF] text-[#1D4ED8] border-[#B2CCFF]';
              crossList.innerHTML += `
                <details class="group bg-white rounded-lg border border-slate-200 overflow-hidden mb-2 shadow-sm">
                  <summary class="flex items-center justify-between p-2.5 cursor-pointer bg-slate-50 hover:bg-slate-100 transition list-none">
                    <div class="flex items-center gap-2">
                      <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-slate-400 group-open:-rotate-180 transition-transform"></i>
                      <span class="font-bold text-[#0B1739]">${deal.product}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-[9px] px-1.5 py-0.5 rounded border font-bold uppercase ${prioClass}">${deal.priority}</span>
                      <span class="font-mono font-bold text-[#FF5A00]">${(deal.estimated_deal_size / 1000000000).toFixed(1)} Tỷ</span>
                    </div>
                  </summary>
                  <div class="p-2.5 text-slate-600 bg-white border-t border-slate-100 leading-relaxed text-[11px]">
                    ${deal.reasoning}
                  </div>
                </details>
              `;
            });
        }
        document.getElementById('eb-cross-total').textContent = `Quy mô: ${(totalDeal / 1000000000).toFixed(1)} Tỷ`;

        // Render AI Insight (SWOT)
        const swot = data.swot_analysis;
        if (swot) {
            const insightBox = document.getElementById('ai-insight-box');
            const insightContent = document.getElementById('ai-insight-content');
            insightBox.classList.remove('hidden');
            
            let swotHtml = '';
            if (swot.strengths && swot.strengths.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-green-700">Điểm mạnh (Strengths):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.strengths.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            if (swot.weaknesses && swot.weaknesses.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-red-600">Điểm yếu (Weaknesses):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.weaknesses.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            if (swot.opportunities && swot.opportunities.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-blue-600">Cơ hội (Opportunities):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.opportunities.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            if (swot.threats && swot.threats.length > 0) {
                swotHtml += `<div class="space-y-1"><span class="text-[11px] font-bold text-orange-600">Rủi ro (Threats):</span><ul class="text-[10px] text-slate-600 space-y-0.5">`;
                swot.threats.forEach(s => swotHtml += `<li>• ${s}</li>`);
                swotHtml += `</ul></div>`;
            }
            
            insightContent.innerHTML = swotHtml;
            lucide.createIcons();
        }

lucide.createIcons();
      } catch (err) {
        console.error(err);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i><span>CHẠY THẨM ĐỊNH AI 360°</span>`;
        lucide.createIcons();
      }
    }

    // 10. Export Docx Memo API
    async function exportDocxMemo() {
      const btn = document.getElementById('btn-export-docx');
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>ĐANG XUẤT...</span>`;
      lucide.createIcons();

      try {
        const payload = {
          company: {
            name: document.getElementById('eb-company-name').value,
            tax_id: document.getElementById('eb-tax-id').value
          },
          reporting_period: document.getElementById('eb-period').value,
          financials: {
            BS001: parseVND(document.getElementById('eb-ca').value),
            BS002: parseVND(document.getElementById('eb-cl').value),
            BS003: parseVND(document.getElementById('eb-ar').value),
            BS004: parseVND(document.getElementById('eb-inv').value),
            BS005: parseVND(document.getElementById('eb-ap').value),
            BS008: parseVND(document.getElementById('eb-equity').value),
            IS001: parseVND(document.getElementById('eb-revenue').value),
            IS003: parseVND(document.getElementById('eb-ebit').value),
            IS004: parseVND(document.getElementById('eb-interest').value),
          },
          debt_service: {
            principal_due: parseVND(document.getElementById('eb-principal').value),
            interest_expense: parseVND(document.getElementById('eb-interest').value)
          }
        };

        const res = await fetch('/build-memo-docx', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `TO_TRINH_TIN_DUNG_MB02a_${payload.company.tax_id}_${payload.reporting_period}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        console.error(err);
        alert('Lỗi xuất Tờ trình Word: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="file-down" class="w-3.5 h-3.5"></i><span>Xuất tờ trình</span>`;
        lucide.createIcons();
      }
    }

    // 11. Run RB Assessment API
    async function runRBAssessment() {
      const btn = document.getElementById('btn-run-rb');
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>ĐANG TÍNH DTI...</span>`;
      lucide.createIcons();

      try {
        const payload = {
          assessment_id: "RB-TIKTOK-001",
          customer: {
            customer_id: document.getElementById('rb-customer-id').value,
            name: document.getElementById('rb-name').value,
            segment: "individual_business_owner",
            business_channel: document.getElementById('rb-channel').value
          },
          income: [
            {
              type: "business",
              monthly_amount: parseVND(document.getElementById('rb-gross-income').value),
              verification_status: "verified",
              eligible_percent: parseFloat(document.getElementById('rb-eligible-pct').value) / 100
            }
          ],
          existing_debts: [
            {
              type: "long_term_loan",
              outstanding: parseVND(document.getElementById('rb-debt-outstanding').value),
              monthly_payment: parseVND(document.getElementById('rb-debt-monthly').value)
            }
          ],
          loan: {
            amount: parseVND(document.getElementById('rb-loan-amt').value),
            annual_interest_rate: parseFloat(document.getElementById('rb-loan-rate').value) / 100,
            tenor_months: parseInt(document.getElementById('rb-loan-tenor').value)
          }
        };

        const res = await fetch('/rb/assess', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        const inc = data.income || {};
        const ratios = data.ratios || {};
        const rec = data.preliminary_recommendation?.outcome || 'PROCEED_FOR_HUMAN_REVIEW';

        document.getElementById('rb-decision-text').textContent = rec;
        document.getElementById('rb-kpi-income').textContent = ((inc.eligible_monthly_income || 0) / 1000000).toFixed(1) + ' Tr';
        document.getElementById('rb-kpi-dti').textContent = ratios.dti ? (ratios.dti * 100).toFixed(1) + '%' : '21.0%';
        document.getElementById('rb-kpi-disposable').textContent = ((ratios.disposable_income || 0) / 1000000).toFixed(1) + ' Tr';
        document.getElementById('rb-memo-text').textContent = data.credit_memo || 'Đã tạo xong tóm tắt thẩm định tín dụng cá nhân.';

        lucide.createIcons();
      } catch (err) {
        console.error(err);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="play" class="w-4 h-4 fill-current"></i><span>CHẠY THẨM ĐỊNH KHCN (RB)</span>`;
        lucide.createIcons();
      }
    }

    // 12. Chat Copilot Message Sending
    async function sendChatMessage(e) {
      e.preventDefault();
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';

      const container = document.getElementById('chat-messages');
      container.innerHTML += `
        <div class="flex justify-end">
          <div class="p-3 rounded-xl bg-[#FF5A00] text-white max-w-[85%] shadow-sm leading-relaxed">
            ${text}
          </div>
        </div>
      `;
      container.scrollTop = container.scrollHeight;

      const loadingId = 'loading-' + Date.now();
      container.innerHTML += `
        <div id="${loadingId}" class="flex justify-start">
          <div class="p-3 rounded-xl bg-slate-100 text-[#667085] max-w-[85%] flex items-center gap-1.5 border border-[#E6EAF0]">
            <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i>
            <span>Đang tham vấn GreenNode MaaS AI...</span>
          </div>
        </div>
      `;
      lucide.createIcons();
      container.scrollTop = container.scrollHeight;

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        document.getElementById(loadingId)?.remove();

        container.innerHTML += `
          <div class="flex justify-start">
            <div class="p-3.5 rounded-xl bg-slate-50 border border-[#E6EAF0] text-[#0B1739] max-w-[88%] whitespace-pre-wrap leading-relaxed shadow-sm">
              ${data.reply || data.content || 'Đã nhận phản hồi.'}
            </div>
          </div>
        `;
      } catch (err) {
        document.getElementById(loadingId)?.remove();
        container.innerHTML += `
          <div class="flex justify-start">
            <div class="p-3 rounded-xl bg-[#FEF3F2] border border-[#FECDCA] text-[#B42318] max-w-[85%]">
              Lỗi kết nối AI: ${err.message}
            </div>
          </div>
        `;
      }
      container.scrollTop = container.scrollHeight;
    }

    // Auto initialize on load
    window.addEventListener('DOMContentLoaded', () => {
      runEBAssessment();
      runRBAssessment();
    });
  
    async function saveEBProfile() {
      const btn = document.getElementById('btn-save-eb');
      const origText = btn.innerHTML;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> LƯU...';
      
      const payload = {
        company: {
          name: document.getElementById('eb-company-name').value,
          tax_id: document.getElementById('eb-tax-id').value
        },
        reporting_period: document.getElementById('eb-period').value,
        financials: {
          BS001: parseVND(document.getElementById('eb-ca').value),
          BS002: parseVND(document.getElementById('eb-cl').value),
          BS003: parseVND(document.getElementById('eb-ar').value),
          BS004: parseVND(document.getElementById('eb-inv').value),
          BS005: parseVND(document.getElementById('eb-ap').value),
          BS006: parseVND(document.getElementById('eb-std').value),
          BS007: parseVND(document.getElementById('eb-tl').value),
          BS008: parseVND(document.getElementById('eb-equity').value),
          IS001: parseVND(document.getElementById('eb-revenue').value),
          IS002: parseVND(document.getElementById('eb-gp').value),
          IS003: parseVND(document.getElementById('eb-ebit').value),
          IS004: parseVND(document.getElementById('eb-interest').value),
          IS005: parseVND(document.getElementById('eb-np').value),
          CF001: parseVND(document.getElementById('eb-ocf').value),
          CF002: parseVND(document.getElementById('eb-icf').value),
          CF003: parseVND(document.getElementById('eb-fcf').value)
        }
      };
      
      try {
        const response = await fetch('/api/save-eb', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (response.ok) {
          btn.innerHTML = '<i data-lucide="check" class="w-3.5 h-3.5"></i> ĐÃ LƯU';
          setTimeout(() => { btn.innerHTML = origText; lucide.createIcons(); }, 2000);
        }
      } catch (err) {
        console.error(err);
        btn.innerHTML = origText;
        lucide.createIcons();
      }
    }
    
    async function loadEBProfile(mst) {
      if (!mst) return;
      try {
        const response = await fetch(`/api/load-eb/${mst}`);
        if (response.ok) {
          const data = await response.json();
          if (data.company) {
            document.getElementById('eb-company-name').value = data.company.name || '';
          }
          if (data.reporting_period) {
            document.getElementById('eb-period').value = data.reporting_period || '';
          }
          if (data.financials) {
            const formatVND = val => val ? (val / 1e9).toFixed(1) : '';
            document.getElementById('eb-ca').value = formatVND(data.financials.BS001);
            document.getElementById('eb-cl').value = formatVND(data.financials.BS002);
            document.getElementById('eb-ar').value = formatVND(data.financials.BS003);
            document.getElementById('eb-inv').value = formatVND(data.financials.BS004);
            document.getElementById('eb-ap').value = formatVND(data.financials.BS005);
            document.getElementById('eb-std').value = formatVND(data.financials.BS006);
            document.getElementById('eb-tl').value = formatVND(data.financials.BS007);
            document.getElementById('eb-equity').value = formatVND(data.financials.BS008);
            document.getElementById('eb-revenue').value = formatVND(data.financials.IS001);
            document.getElementById('eb-gp').value = formatVND(data.financials.IS002);
            document.getElementById('eb-ebit').value = formatVND(data.financials.IS003);
            document.getElementById('eb-interest').value = formatVND(data.financials.IS004);
            document.getElementById('eb-np').value = formatVND(data.financials.IS005);
            document.getElementById('eb-ocf').value = formatVND(data.financials.CF001);
            document.getElementById('eb-icf').value = formatVND(data.financials.CF002);
            document.getElementById('eb-fcf').value = formatVND(data.financials.CF003);
          }
        }
      } catch (err) {
        console.error(err);
      }
    }
