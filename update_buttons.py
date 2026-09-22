import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

btn_area = '''        <!-- Right: Primary CTA Execution Buttons -->
        <div class="flex items-center space-x-2">
          <button onclick="runEBAssessment()" id="btn-run-eb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            <span>CHẠY THẨM ĐỊNH AI 360°</span>
          </button>
        </div>'''

new_btn_area = '''        <!-- Right: Primary CTA Execution Buttons -->
        <div class="flex items-center space-x-2">
          <button onclick="saveEBProfile()" id="btn-save-eb" class="px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="save" class="w-3.5 h-3.5"></i>
            <span>LƯU HỒ SƠ</span>
          </button>
          <button onclick="runEBAssessment()" id="btn-run-eb" class="px-4 py-2 rounded-lg bg-[#FF5A00] hover:bg-[#EA4E00] text-white font-bold text-xs flex items-center gap-2 shadow-sm transition">
            <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
            <span>CHẠY THẨM ĐỊNH AI 360°</span>
          </button>
        </div>'''

html = html.replace(btn_area, new_btn_area)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
