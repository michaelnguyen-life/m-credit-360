import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = "const btn = document.getElementById('btn-run-eb');"
loading_js = '''
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
'''

if 'OSINT loading state' not in html:
    html = html.replace(target, target + '\n' + loading_js)
    
with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
