import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Modify handleFileSelect to actually upload the file via fetch!
# Wait, handleFileSelect is currently:
old_handleFileSelect = '''    function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      currentUploadedFileName = files[0].name || "BCTC_Uploaded.pdf";'''

new_handleFileSelect = '''    let realExtractedData = null;
    function handleFileSelect(e) {
      const files = e.target.files;
      if (!files.length) return;
      currentUploadedFileName = files[0].name || "BCTC_Uploaded.pdf";
      
      const formData = new FormData();
      formData.append("file", files[0]);
      
      fetch('/api/upload', {
          method: 'POST',
          body: formData
      })
      .then(res => res.json())
      .then(data => {
          if(data.status === 'success') {
              realExtractedData = data;
          }
      })
      .catch(err => console.error("Upload error:", err));
'''

html = html.replace(old_handleFileSelect, new_handleFileSelect)

# Now modify applyExtractedData
old_apply = '''    function applyExtractedData() {
      closeExtractionReview();
      loadSampleEB('alpha');'''

new_apply = '''    function applyExtractedData() {
      closeExtractionReview();
      
      // Load real extracted data!
      if (realExtractedData) {
          document.getElementById('eb-tax-id').value = realExtractedData.company.tax_id || "";
          document.getElementById('eb-company-name').value = realExtractedData.company.name || "";
          
          const fin = realExtractedData.financials || {};
          document.getElementById('eb-revenue').value = fin.IS_REVENUE || 0;
          document.getElementById('eb-ebit').value = fin.IS_NET_PROFIT || 0; // mapped to ebit for now
          document.getElementById('eb-interest').value = fin.IS_INTEREST_EXPENSE || 0;
          document.getElementById('eb-ar').value = fin.BS_TRADE_RECEIVABLES || 0;
          document.getElementById('eb-ap').value = fin.BS_TRADE_PAYABLES || 0;
          document.getElementById('eb-inv').value = fin.BS_INVENTORY || 0;
          document.getElementById('eb-cl').value = fin.BS_CURRENT_LIABILITIES || 0;
          document.getElementById('eb-ca').value = fin.BS_CURRENT_ASSETS || 0;
          document.getElementById('eb-short-debt').value = fin.BS_SHORT_TERM_DEBT || 0;
          
          // Re-format inputs
          document.querySelectorAll('.executive-input').forEach(input => {
              const val = parseVND(input.value);
              input.value = formatVND(val);
          });
      } else {
          loadSampleEB('alpha'); // Fallback if upload failed
      }
      '''

html = html.replace(old_apply, new_apply)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
