import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_fetch = '''      fetch('/api/upload', {
          method: 'POST',
          body: formData
      })
      .then(res => res.json())
      .then(data => {
          if(data.status === 'success') {
              realExtractedData = data;
          }
      })
      .catch(err => console.error("Upload error:", err));'''

new_fetch = '''      fetch('/api/upload', {
          method: 'POST',
          body: formData
      })
      .then(res => res.json())
      .then(data => {
          if(data.status === 'success') {
              realExtractedData = data;
              // Populate Modal
              document.getElementById('modal-company-name').textContent = data.company.name || "Không xác định";
              document.getElementById('modal-tax-id').textContent = data.company.tax_id || "Không xác định";
              document.getElementById('modal-revenue').textContent = formatVND(data.financials.IS_REVENUE || 0);
              document.getElementById('modal-ebit').textContent = formatVND(data.financials.IS_NET_PROFIT || 0);
              document.getElementById('modal-ca').textContent = formatVND(data.financials.BS_CURRENT_ASSETS || 0);
              document.getElementById('modal-cl').textContent = formatVND(data.financials.BS_CURRENT_LIABILITIES || 0);
              document.getElementById('modal-filename-alert').textContent = data.filename || "vừa tải lên";
          }
      })
      .catch(err => console.error("Upload error:", err));'''

html = html.replace(old_fetch, new_fetch)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
