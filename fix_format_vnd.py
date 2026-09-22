import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_code = '''    function parseVND(val) {
      if (typeof val === 'number') return val;
      return parseFloat(String(val).replace(/\./g, '').replace(/,/g, '').replace(/[^\d.-]/g, '')) || 0;
    }'''

new_code = '''    function parseVND(val) {
      if (typeof val === 'number') return val;
      return parseFloat(String(val).replace(/\./g, '').replace(/,/g, '').replace(/[^\d.-]/g, '')) || 0;
    }
    function formatVND(val) {
      return new Intl.NumberFormat('vi-VN').format(val);
    }'''

html = html.replace(old_code, new_code)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
