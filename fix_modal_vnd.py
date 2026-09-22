import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_code = '''              document.getElementById('modal-revenue').textContent = formatVND(data.financials.IS_REVENUE || 0);
              document.getElementById('modal-ebit').textContent = formatVND(data.financials.IS_NET_PROFIT || 0);
              document.getElementById('modal-ca').textContent = formatVND(data.financials.BS_CURRENT_ASSETS || 0);
              document.getElementById('modal-cl').textContent = formatVND(data.financials.BS_CURRENT_LIABILITIES || 0);'''

new_code = '''              document.getElementById('modal-revenue').textContent = formatVND(data.financials.IS_REVENUE || 0) + " VND";
              document.getElementById('modal-ebit').textContent = formatVND(data.financials.IS_NET_PROFIT || 0) + " VND";
              document.getElementById('modal-ca').textContent = formatVND(data.financials.BS_CURRENT_ASSETS || 0) + " VND";
              document.getElementById('modal-cl').textContent = formatVND(data.financials.BS_CURRENT_LIABILITIES || 0) + " VND";'''

html = html.replace(old_code, new_code)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
