import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the loadSampleRB function
old_load_rb = """    async function loadSampleRB(type) {
      try {
        let d = null;
        try {
          const res = await fetch(`/api/sample/rb/${type}`);
          if (res.ok) {
            d = await res.json();
          }
        } catch (netErr) {
          console.warn('API sample load failed, falling back to client cache:', netErr);
        }
        if (!d) {
          d = CLIENT_FALLBACK_RB;
        }
        
        document.getElementById('rb-customer-id').value = d.customer?.customer_id || 'KH01';
        document.getElementById('rb-name').value = d.customer?.name || 'PHẠM THANH BÌNH';
        document.getElementById('rb-channel').value = d.customer?.business_channel || 'TikTok Shop';
        
        const inc = d.income?.[0] || {};
        document.getElementById('rb-gross-income').value = (inc.monthly_amount || 2919000000).toLocaleString('vi-VN');
        document.getElementById('rb-eligible-pct').value = (inc.eligible_percent || 0.08) * 100;
        
        const debts = d.existing_debts || [];
        const totalOut = debts.reduce((acc, x) => acc + (x.outstanding || 0), 0);
        const totalPay = debts.reduce((acc, x) => acc + (x.monthly_payment || 0), 0);
        document.getElementById('rb-debt-outstanding').value = totalOut.toLocaleString('vi-VN');
        document.getElementById('rb-debt-monthly').value = totalPay.toLocaleString('vi-VN');

        const loan = d.loan || {};
        document.getElementById('rb-loan-amt').value = (loan.amount || 450000000).toLocaleString('vi-VN');
        document.getElementById('rb-loan-rate').value = ((loan.annual_interest_rate || 0.225) * 100).toFixed(1);
        document.getElementById('rb-loan-tenor').value = loan.tenor_months || 48;

        await runRBAssessment();
      } catch (err) {
        console.error(err);
        alert('Lỗi nạp dữ liệu mẫu RB: ' + err.message);
      }
    }"""

new_load_rb = """    async function loadSampleRB(type) {
      try {
        let d = null;
        try {
          const res = await fetch(`/api/sample/rb/${type}`);
          if (res.ok) {
            d = await res.json();
          }
        } catch (netErr) {
          console.warn('API sample load failed, falling back to client cache:', netErr);
        }
        if (!d) {
          d = CLIENT_FALLBACK_RB;
        }
        
        // Save to global variable but don't fill inputs yet (Per User Requirement)
        window.pendingRBData = d;
        showToast('Đã trích xuất thông tin từ file. Bấm "Chạy Thẩm Định" để hiện kết quả.', 'info');
      } catch (err) {
        console.error(err);
        alert('Lỗi nạp dữ liệu mẫu RB: ' + err.message);
      }
    }"""

content = content.replace(old_load_rb, new_load_rb)

# Now update runRBAssessment to fill inputs from window.pendingRBData if available
old_run_rb = """    async function runRBAssessment() {
      const btn = document.getElementById('btn-run-rb');"""

new_run_rb = """    async function runRBAssessment() {
      if (window.pendingRBData) {
          const d = window.pendingRBData;
          document.getElementById('rb-customer-id').value = d.customer?.customer_id || '';
          document.getElementById('rb-name').value = d.customer?.name || '';
          document.getElementById('rb-channel').value = d.customer?.business_channel || '';
          
          const inc = d.income?.[0] || {};
          document.getElementById('rb-gross-income').value = (inc.monthly_amount) ? inc.monthly_amount.toLocaleString('vi-VN') : '';
          document.getElementById('rb-eligible-pct').value = (inc.eligible_percent) ? (inc.eligible_percent * 100) : '';
          
          const debts = d.existing_debts || [];
          const totalOut = debts.reduce((acc, x) => acc + (x.outstanding || 0), 0);
          const totalPay = debts.reduce((acc, x) => acc + (x.monthly_payment || 0), 0);
          document.getElementById('rb-debt-outstanding').value = (totalOut) ? totalOut.toLocaleString('vi-VN') : '';
          document.getElementById('rb-debt-monthly').value = (totalPay) ? totalPay.toLocaleString('vi-VN') : '';

          const loan = d.loan || {};
          document.getElementById('rb-loan-amt').value = (loan.amount) ? loan.amount.toLocaleString('vi-VN') : '';
          document.getElementById('rb-loan-rate').value = (loan.annual_interest_rate) ? (loan.annual_interest_rate * 100).toFixed(1) : '';
          document.getElementById('rb-loan-tenor').value = loan.tenor_months || '';
          window.pendingRBData = null; // consume it
      }

      const btn = document.getElementById('btn-run-rb');"""

content = content.replace(old_run_rb, new_run_rb)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated RB workflow")
