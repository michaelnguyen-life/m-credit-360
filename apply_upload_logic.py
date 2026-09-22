import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update applyExtractedData to add the uploaded file to Box 1
old_js = '''    function applyExtractedData() {
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
    }'''

new_js = '''    function applyExtractedData() {
      closeExtractionReview();
      loadSampleEB('alpha');
      setTimeout(() => {
        const sourceTag = document.getElementById('eb-source-tag');
        if (sourceTag) {
          sourceTag.textContent = "Nguồn: " + currentUploadedFileName + " (Đã bóc tách AI)";
        }
        // Update Box 1 (Hồ sơ khách hàng) with the actual uploaded file name
        document.getElementById('file-ingested-list').innerHTML = `
          <div class="p-2 rounded-lg bg-slate-50 border flex items-center justify-between">
            <div class="flex items-center gap-2 truncate">
              <span class="w-5 h-5 rounded bg-red-100 text-red-600 font-bold text-[9px] flex items-center justify-center font-mono">FILE</span>
              <div class="truncate">
                <span class="font-semibold text-[#0B1739] block truncate text-[11px]">${currentUploadedFileName}</span>
                <span class="text-[9px] text-[#98A2B3]">Vừa tải lên • Đã bóc tách</span>
              </div>
            </div>
            <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-0.5 flex-shrink-0"><i data-lucide="check" class="w-3 h-3"></i> Phân tích xong</span>
          </div>
        `;
        lucide.createIcons();
      }, 50);
      document.getElementById('eb-empty-state').classList.add('hidden');
      document.getElementById('eb-results-container').classList.remove('hidden');
    }'''

html = html.replace(old_js, new_js)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
