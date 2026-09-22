import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_js = '''    let realExtractedData = null;
    function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      currentUploadedFileName = files[0].name || "BCTC_Uploaded.pdf";
      
      const formData = new FormData();'''

new_js = '''    let realExtractedData = null;
    function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      currentUploadedFileName = files[0].name || "BCTC_Uploaded.pdf";
      
      let ext = "FILE";
      const parts = currentUploadedFileName.split('.');
      if (parts.length > 1) {
          ext = parts[parts.length - 1].toUpperCase().substring(0, 4);
      }
      
      document.getElementById('upload-file-rows').innerHTML = `
        <div class="p-2.5 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between text-xs">
          <div class="flex items-center gap-2 truncate">
            <span class="w-8 h-5 rounded bg-blue-100 text-blue-600 font-bold text-[9px] flex items-center justify-center font-mono">${ext}</span>
            <span class="font-medium text-[#0B1739] truncate">${currentUploadedFileName}</span>
          </div>
          <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-0.5" id="drawer-file-status">Đang tải...</span>
        </div>
      `;
      
      const formData = new FormData();'''

html = html.replace(old_js, new_js)

# And update the "Đang tải..." to "Đã bóc tách" when 100% is reached
old_js2 = '''        if (pct >= 100) {
          clearInterval(interval);
          stageText.textContent = "✓ Hoàn tất bóc tách dữ liệu!";
          setTimeout(() => {
            closeUploadDrawer();'''

new_js2 = '''        if (pct >= 100) {
          clearInterval(interval);
          stageText.textContent = "✓ Hoàn tất bóc tách dữ liệu!";
          const statusEl = document.getElementById('drawer-file-status');
          if(statusEl) statusEl.innerHTML = `<i data-lucide="check" class="w-3 h-3"></i> Đã bóc tách`;
          lucide.createIcons();
          setTimeout(() => {
            closeUploadDrawer();'''

html = html.replace(old_js2, new_js2)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
