rb_section_html = """
      <!-- ==================== TAB 2: RETAIL BANKING WORKSPACE (RB) ==================== -->
      <div id="section-rb" class="hidden space-y-4">
        
        <!-- RB Workflow Action Bar -->
        <div class="executive-card p-3 flex flex-wrap items-center justify-between gap-3 bg-white">
          <!-- Left: Ingestion -->
          <div class="flex items-center space-x-2">
            <button onclick="loadSampleRB('KH01')" class="px-3.5 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition">
              <i data-lucide="user-plus" class="w-3.5 h-3.5"></i>
              <span>+ Khách hàng cá nhân mới</span>
            </button>
            <button onclick="openUploadDrawer()" class="px-3.5 py-2 rounded-lg bg-white border border-[#D0D5DD] hover:bg-slate-50 text-[#0B1739] font-semibold text-xs flex items-center gap-1.5 transition">
              <i data-lucide="upload-cloud" class="w-3.5 h-3.5 text-[#2563EB]"></i>
              <span>Upload sao kê/CCCD</span>
            </button>
          </div>

          <!-- Center: Quick Sample Data -->
          <div class="hidden md:flex items-center space-x-2 text-xs">
            <span class="text-[#667085] font-medium flex items-center gap-1 text-[11px]">
              <i data-lucide="database" class="w-3.5 h-3.5"></i> Mẫu cá nhân nhanh:
            </span>
            <button onclick="loadSampleRB('KH01')" class="px-3 py-1.5 rounded-lg bg-[#F8F9FA] hover:bg-slate-100 text-[#344054] border border-[#E6EAF0] flex items-center gap-1.5 transition text-[11px]">
              <i data-lucide="shopping-bag" class="w-3 h-3 text-[#FF5A00]"></i>
              <span class="font-semibold">Phạm Thanh Bình</span>
              <span class="text-slate-400">TikTok Shop • 2,9 tỷ/tháng</span>
            </button>
          </div>

          <!-- Right: Action CTA -->
          <div class="flex items-center space-x-2">
            <button onclick="runRBAssessment()" id="btn-run-rb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
              <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
              <span>CHẠY THẨM ĐỊNH KHCN (RB)</span>
            </button>
            <button onclick="exportRBDocxMemo()" id="btn-export-rb-docx" class="px-3.5 py-2 rounded-lg bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition">
              <i data-lucide="file-down" class="w-3.5 h-3.5"></i>
              <span>Xuất tờ trình MB01A</span>
            </button>
          </div>
        </div>

        <!-- 3-Column Layout for RB -->
        <div class="grid grid-cols-1 xl:grid-cols-12 gap-4 w-full">
          <!-- Col 1: Customer Profile & Income Inputs -->
          <div class="xl:col-span-4 executive-card p-4 space-y-3.5">
            <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2.5">
              <h2 class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5 uppercase tracking-wide">
                <i data-lucide="user" class="w-4 h-4 text-[#FF5A00]"></i>
                <span>Hồ sơ khách hàng cá nhân / Hộ KD</span>
              </h2>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-[#2563EB] border border-blue-200 font-semibold">
                Phân hệ KHCN (RB)
              </span>
            </div>

            <div class="space-y-3 text-xs">
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-[#667085] font-medium text-[11px] mb-1">Mã KH (Customer ID)</label>
                  <input id="rb-customer-id" type="text" value="KH01" class="executive-input w-full px-2.5 py-1.5 font-mono text-xs" />
                </div>
                <div>
                  <label class="block text-[#667085] font-medium text-[11px] mb-1">Kênh kinh doanh</label>
                  <input id="rb-channel" type="text" value="TikTok Shop & Shopee Mall" class="executive-input w-full px-2.5 py-1.5 text-xs text-[#0B1739]" />
                </div>
              </div>

              <div>
                <label class="block text-[#667085] font-medium text-[11px] mb-1">Họ và tên khách hàng</label>
                <input id="rb-name" type="text" value="PHẠM THANH BÌNH" class="executive-input w-full px-2.5 py-1.5 font-semibold text-xs text-[#0B1739]" />
              </div>

              <!-- Income & Debts -->
              <div class="p-3 rounded-xl bg-slate-50 border border-[#E6EAF0] space-y-2.5">
                <span class="text-[11px] font-bold text-[#0B1739] block">1. Thu nhập & Dòng tiền hàng tháng (VND)</span>
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Doanh thu bình quân/tháng</label>
                    <input id="rb-gross-income" type="text" value="2.919.000.000" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Tỷ lệ công nhận (%)</label>
                    <input id="rb-eligible-pct" type="number" value="8" step="0.5" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                </div>
              </div>

              <div class="p-3 rounded-xl bg-slate-50 border border-[#E6EAF0] space-y-2.5">
                <span class="text-[11px] font-bold text-[#0B1739] block">2. Nghĩa vụ nợ hiện hữu (CIC)</span>
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Tổng dư nợ hiện tại</label>
                    <input id="rb-debt-outstanding" type="text" value="2.739.000.000" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Trả nợ hàng tháng</label>
                    <input id="rb-debt-monthly" type="text" value="35.000.000" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                </div>
              </div>

              <!-- Loan Request -->
              <div class="p-3 rounded-xl bg-orange-50/60 border border-orange-100 space-y-2.5">
                <span class="text-[11px] font-bold text-[#FF5A00] block">3. Khoản vay đề nghị cấp</span>
                <div class="grid grid-cols-3 gap-2">
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Số tiền vay</label>
                    <input id="rb-loan-amt" type="text" value="450.000.000" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Lãi suất (%/năm)</label>
                    <input id="rb-loan-rate" type="text" value="22.5" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                  <div>
                    <label class="block text-[#667085] text-[10px] mb-0.5">Thời hạn (tháng)</label>
                    <input id="rb-loan-tenor" type="number" value="48" class="executive-input w-full px-2 py-1 font-mono text-xs text-right" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Col 2: RB Assessment Results & KPIs -->
          <div class="xl:col-span-5 space-y-3.5">
            <!-- Decision Banner -->
            <div id="rb-decision-banner" class="executive-card p-4 border border-[#A6F4C5] bg-[#ECFDF3] flex items-center justify-between transition-all">
              <div class="space-y-0.5">
                <span class="text-[10px] font-bold text-[#667085] uppercase tracking-wider block">KẾT QUẢ THẨM ĐỊNH SƠ BỘ KHCN</span>
                <h3 id="rb-decision-text" class="text-base font-black text-[#027A48]">PROCEED_FOR_HUMAN_REVIEW</h3>
                <p class="text-[11px] text-[#667085]">Khách hàng đủ điều kiện nộp hồ sơ phê duyệt tín dụng MSB.</p>
              </div>
              <div id="rb-decision-icon" class="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#00A86B] shadow-sm flex-shrink-0">
                <i data-lucide="check-circle" class="w-6 h-6"></i>
              </div>
            </div>

            <!-- KPIs -->
            <div class="grid grid-cols-3 gap-2.5">
              <div class="executive-card p-3 text-center">
                <span class="text-[10px] text-[#667085] block font-medium">Thu nhập đủ ĐK</span>
                <span id="rb-kpi-income" class="text-base font-black text-[#0B1739] font-mono block mt-0.5">233,5 Tr</span>
                <span class="text-[9px] text-[#00A86B] font-semibold block mt-0.5">Đã xác minh 100%</span>
              </div>
              <div class="executive-card p-3 text-center">
                <span class="text-[10px] text-[#667085] block font-medium">Hệ số nợ (DTI)</span>
                <span id="rb-kpi-dti" class="text-base font-black text-[#00A86B] font-mono block mt-0.5">21.0%</span>
                <span class="text-[9px] text-slate-500 font-semibold block mt-0.5">Chuẩn MSB ≤ 55%</span>
              </div>
              <div class="executive-card p-3 text-center">
                <span class="text-[10px] text-[#667085] block font-medium">Thu nhập tích lũy</span>
                <span id="rb-kpi-disposable" class="text-base font-black text-[#00A86B] font-mono block mt-0.5">178,5 Tr</span>
                <span class="text-[9px] text-[#00A86B] font-semibold block mt-0.5">Khả năng trả nợ cao</span>
              </div>
            </div>

            <!-- RB Credit Memo Summary Text -->
            <div class="executive-card p-4 space-y-2">
              <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2">
                <span class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5">
                  <i data-lucide="file-text" class="w-4 h-4 text-[#2563EB]"></i>
                  <span>Tóm tắt thẩm định tín dụng cá nhân</span>
                </span>
                <button onclick="exportRBDocxMemo()" class="text-[11px] text-[#2563EB] hover:underline font-bold flex items-center gap-1">
                  <i data-lucide="download" class="w-3 h-3"></i> Tải MB01A Word
                </button>
              </div>
              <div id="rb-memo-text" class="text-[11px] text-[#344054] whitespace-pre-wrap font-mono bg-slate-50 p-3 rounded-lg border border-[#E6EAF0] max-h-64 overflow-y-auto leading-relaxed">
Đang tải tóm tắt thẩm định...
              </div>
            </div>
          </div>

          <!-- Col 3: Document Checklist & Notes -->
          <div class="xl:col-span-3 space-y-3.5">
            <div class="executive-card p-3.5 space-y-2.5">
              <div class="flex items-center justify-between border-b border-[#E6EAF0] pb-2">
                <span class="text-xs font-bold text-[#0B1739] flex items-center gap-1.5">
                  <i data-lucide="check-square" class="w-4 h-4 text-[#00A86B]"></i>
                  <span>Checklist hồ sơ KHCN</span>
                </span>
                <span class="text-[10px] font-bold text-[#00A86B]">5/5 Đạt</span>
              </div>
              <div class="space-y-1.5 text-xs">
                <div class="p-2 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between">
                  <span class="text-[#344054]">CCCD gắn chip</span>
                  <span class="text-[10px] text-[#00A86B] font-bold">✓ Hợp lệ</span>
                </div>
                <div class="p-2 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between">
                  <span class="text-[#344054]">Sao kê TK ngân hàng</span>
                  <span class="text-[10px] text-[#00A86B] font-bold">✓ Đủ 6 tháng</span>
                </div>
                <div class="p-2 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between">
                  <span class="text-[#344054]">Doanh thu TikTok Shop</span>
                  <span class="text-[10px] text-[#00A86B] font-bold">✓ Đối soát khớp</span>
                </div>
                <div class="p-2 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between">
                  <span class="text-[#344054]">Tra cứu CIC cá nhân</span>
                  <span class="text-[10px] text-[#00A86B] font-bold">✓ Nhóm 1 (Tốt)</span>
                </div>
                <div class="p-2 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between">
                  <span class="text-[#344054]">Giấy đề nghị cấp TD</span>
                  <span class="text-[10px] text-[#2563EB] font-bold">Mẫu MB01A</span>
                </div>
              </div>
            </div>

            <!-- Action Export CTA Box -->
            <div class="executive-card p-4 text-center space-y-2 bg-blue-50/50 border-blue-200">
              <i data-lucide="file-check-2" class="w-8 h-8 text-[#2563EB] mx-auto"></i>
              <h4 class="text-xs font-bold text-[#0B1739]">Xuất Tờ Trình MB01A</h4>
              <p class="text-[10px] text-[#667085] leading-relaxed">
                Biểu mẫu QT.RR.038 chuẩn Hội Sở MSB, tự động điền thông tin nhân thân, doanh số bán lẻ TMĐT và phương án trả nợ.
              </p>
              <button onclick="exportRBDocxMemo()" class="w-full py-2 rounded-lg bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-bold text-xs shadow-sm transition">
                Tải file Word MB01A
              </button>
            </div>
          </div>
        </div>

      </div>
"""
