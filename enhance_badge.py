import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_js = '''        // Update Box 1 (Hồ sơ khách hàng) with the actual uploaded file name
        document.getElementById('file-ingested-list').innerHTML = `
          <div class="p-2 rounded-lg bg-slate-50 border flex items-center justify-between">
            <div class="flex items-center gap-2 truncate">
              <span class="w-5 h-5 rounded bg-red-100 text-red-600 font-bold text-[9px] flex items-center justify-center font-mono">FILE</span>
              <div class="truncate">
                <span class="font-semibold text-[#0B1739] block truncate text-[11px]">${currentUploadedFileName}</span>'''

new_js = '''        // Update Box 1 (Hồ sơ khách hàng) with the actual uploaded file name
        let ext = "FILE";
        const parts = currentUploadedFileName.split('.');
        if (parts.length > 1) {
            ext = parts[parts.length - 1].toUpperCase().substring(0, 4);
        }
        document.getElementById('file-ingested-list').innerHTML = `
          <div class="p-2 rounded-lg bg-slate-50 border flex items-center justify-between">
            <div class="flex items-center gap-2 truncate">
              <span class="w-8 h-5 rounded bg-blue-100 text-blue-600 font-bold text-[9px] flex items-center justify-center font-mono">${ext}</span>
              <div class="truncate">
                <span class="font-semibold text-[#0B1739] block truncate text-[11px]">${currentUploadedFileName}</span>'''

html = html.replace(old_js, new_js)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
