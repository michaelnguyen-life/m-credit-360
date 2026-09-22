import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the Extracted Fields Table to have IDs so we can modify them dynamically
old_table = '''<!-- Extracted Fields Table -->
      <div class="overflow-y-auto space-y-2 text-xs flex-1">
        <div class="p-2.5 rounded-lg bg-slate-50 border border-[#E6EAF0] grid grid-cols-2 gap-2">
          <div><span class="text-[#667085] block text-[10px]">Tên Doanh Nghiệp:</span><strong class="text-[#0B1739] text-xs">CÔNG TY CỔ PHẦN TẬP ĐOÀN ALPHA</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Mã số thuế (MST):</span><strong class="text-[#0B1739] font-mono text-xs">0311807068</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Doanh thu thuần:</span><strong class="text-[#0B1739] font-mono text-xs">318.000.000.000 VND</strong></div>
          <div><span class="text-[#667085] block text-[10px]">EBIT:</span><strong class="text-[#0B1739] font-mono text-xs">18.500.000.000 VND</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Tài sản ngắn hạn:</span><strong class="text-[#0B1739] font-mono text-xs">120.000.000.000 VND</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Nợ ngắn hạn:</span><strong class="text-[#0B1739] font-mono text-xs">145.000.000.000 VND</strong></div>
        </div>
      </div>'''

new_table = '''<!-- Extracted Fields Table -->
      <div class="overflow-y-auto space-y-2 text-xs flex-1">
        <div class="p-2.5 rounded-lg bg-slate-50 border border-[#E6EAF0] grid grid-cols-2 gap-2">
          <div><span class="text-[#667085] block text-[10px]">Tên Doanh Nghiệp:</span><strong id="modal-company-name" class="text-[#0B1739] text-xs">...</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Mã số thuế (MST):</span><strong id="modal-tax-id" class="text-[#0B1739] font-mono text-xs">...</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Doanh thu thuần:</span><strong id="modal-revenue" class="text-[#0B1739] font-mono text-xs">...</strong></div>
          <div><span class="text-[#667085] block text-[10px]">EBIT:</span><strong id="modal-ebit" class="text-[#0B1739] font-mono text-xs">...</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Tài sản ngắn hạn:</span><strong id="modal-ca" class="text-[#0B1739] font-mono text-xs">...</strong></div>
          <div><span class="text-[#667085] block text-[10px]">Nợ ngắn hạn:</span><strong id="modal-cl" class="text-[#0B1739] font-mono text-xs">...</strong></div>
        </div>
      </div>'''

html = html.replace(old_table, new_table)

# And update the warning message
old_warning = '''<p class="mt-0.5 text-[11px] leading-relaxed">
            Hồ sơ tải lên có doanh thu <strong>318,00 tỷ VND</strong> (Trùng khớp số liệu kiểm toán).
          </p>'''
new_warning = '''<p class="mt-0.5 text-[11px] leading-relaxed">
            Hồ sơ <strong id="modal-filename-alert">...</strong> đã được bóc tách và sẵn sàng để áp dụng vào hệ thống.
          </p>'''

html = html.replace(old_warning, new_warning)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
