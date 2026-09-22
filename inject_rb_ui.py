import io

with io.open('generate_rb_ui.py', 'r', encoding='utf-8') as f:
    rb_script = f.read()

# Extract the rb_section_html string from the script
start_str = 'rb_section_html = """'
end_str = '"""'
start_idx = rb_script.find(start_str) + len(start_str)
end_idx = rb_script.rfind(end_str)
rb_html = rb_script[start_idx:end_idx]

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Target insertion right before <!-- ==================== TAB 3: ZALO BOT GATEWAY ==================== -->
target = '<!-- ==================== TAB 3: ZALO BOT GATEWAY ==================== -->'

if target in html:
    html = html.replace(target, rb_html + '\n\n      ' + target)
    print("Successfully inserted section-rb into index.html!")
else:
    print("Target comment for Zalo not found!")

# Now add exportRBDocxMemo in script section
export_js = """
    // 10b. Export RB Docx Memo (MB01A) API
    async function exportRBDocxMemo() {
      const btn = document.getElementById('btn-export-rb-docx');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>ĐANG XUẤT MB01A...</span>`;
        lucide.createIcons();
      }

      try {
        const payload = {
          customer: {
            customer_id: document.getElementById('rb-customer-id').value,
            name: document.getElementById('rb-name').value,
            segment: "individual_business_owner",
            business_channel: document.getElementById('rb-channel').value
          },
          income: [
            {
              type: "business",
              monthly_amount: parseVND(document.getElementById('rb-gross-income').value),
              verification_status: "verified",
              eligible_percent: parseFloat(document.getElementById('rb-eligible-pct').value) / 100
            }
          ],
          existing_debts: [
            {
              type: "long_term_loan",
              outstanding: parseVND(document.getElementById('rb-debt-outstanding').value),
              monthly_payment: parseVND(document.getElementById('rb-debt-monthly').value)
            }
          ],
          loan: {
            amount: parseVND(document.getElementById('rb-loan-amt').value),
            annual_interest_rate: parseFloat(document.getElementById('rb-loan-rate').value) / 100,
            tenor_months: parseInt(document.getElementById('rb-loan-tenor').value),
            purpose: "Bổ sung vốn lưu động kinh doanh hàng tiêu dùng e-Commerce"
          }
        };

        const res = await fetch('/rb/export-memo-docx', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `TO_TRINH_KHCN_MB01A_${payload.customer.customer_id}_${payload.customer.name.replace(/\\s+/g, '_')}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        console.error(err);
        alert('Lỗi xuất Tờ trình MB01A Word: ' + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = `<i data-lucide="file-down" class="w-3.5 h-3.5"></i><span>Xuất tờ trình MB01A</span>`;
          lucide.createIcons();
        }
      }
    }
"""

js_target = "// 11. Run RB Assessment API"
if js_target in html:
    html = html.replace(js_target, export_js + "\n    " + js_target)
    print("Added exportRBDocxMemo function to JS!")
else:
    print("JS target not found!")

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html successfully!")
