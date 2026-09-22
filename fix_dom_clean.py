import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix applyExtractedData: remove nonexistent eb-short-debt
old_apply = """          document.getElementById('eb-cl').value = fin.BS_CURRENT_LIABILITIES || 0;
          document.getElementById('eb-ca').value = fin.BS_CURRENT_ASSETS || 0;
          document.getElementById('eb-short-debt').value = fin.BS_SHORT_TERM_DEBT || 0;"""

new_apply = """          document.getElementById('eb-cl').value = fin.BS_CURRENT_LIABILITIES || 0;
          document.getElementById('eb-ca').value = fin.BS_CURRENT_ASSETS || 0;"""

if old_apply in html:
    html = html.replace(old_apply, new_apply)
    print("Fixed applyExtractedData (removed eb-short-debt)")
else:
    print("old_apply not matched directly, checking...")

# 2. Clean up dead saveEBProfile and loadEBProfile that referenced missing IDs
old_dead_script = """    async function saveEBProfile() {
      const btn = document.getElementById('btn-save-eb');
      const origText = btn.innerHTML;
      btn.innerHTML = '<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> LƯU...';
      
      const payload = {
        company: {
          name: document.getElementById('eb-company-name').value,
          tax_id: document.getElementById('eb-tax-id').value
        },
        reporting_period: document.getElementById('eb-period').value,
        financials: {
          BS001: parseVND(document.getElementById('eb-ca').value),
          BS002: parseVND(document.getElementById('eb-cl').value),
          BS003: parseVND(document.getElementById('eb-ar').value),
          BS004: parseVND(document.getElementById('eb-inv').value),
          BS005: parseVND(document.getElementById('eb-ap').value),
          BS006: parseVND(document.getElementById('eb-std').value),
          BS007: parseVND(document.getElementById('eb-tl').value),
          BS008: parseVND(document.getElementById('eb-equity').value),
          IS001: parseVND(document.getElementById('eb-revenue').value),
          IS002: parseVND(document.getElementById('eb-gp').value),
          IS003: parseVND(document.getElementById('eb-ebit').value),
          IS004: parseVND(document.getElementById('eb-interest').value),
          IS005: parseVND(document.getElementById('eb-np').value),
          CF001: parseVND(document.getElementById('eb-ocf').value),
          CF002: parseVND(document.getElementById('eb-icf').value),
          CF003: parseVND(document.getElementById('eb-fcf').value)
        }
      };
      
      try {
        const response = await fetch('/api/save-eb', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (response.ok) {
          btn.innerHTML = '<i data-lucide="check" class="w-3.5 h-3.5"></i> ĐÃ LƯU';
          setTimeout(() => { btn.innerHTML = origText; lucide.createIcons(); }, 2000);
        }
      } catch (err) {
        console.error(err);
        btn.innerHTML = origText;
        lucide.createIcons();
      }
    }
    
    async function loadEBProfile(mst) {
      if (!mst) return;
      try {
        const response = await fetch(`/api/load-eb/${mst}`);
        if (response.ok) {
          const data = await response.json();
          if (data.company) {
            document.getElementById('eb-company-name').value = data.company.name || '';
          }
          if (data.reporting_period) {
            document.getElementById('eb-period').value = data.reporting_period || '';
          }
          if (data.financials) {
            const formatVND = val => val ? (val / 1e9).toFixed(1) : '';
            document.getElementById('eb-ca').value = formatVND(data.financials.BS001);
            document.getElementById('eb-cl').value = formatVND(data.financials.BS002);
            document.getElementById('eb-ar').value = formatVND(data.financials.BS003);
            document.getElementById('eb-inv').value = formatVND(data.financials.BS004);
            document.getElementById('eb-ap').value = formatVND(data.financials.BS005);
            document.getElementById('eb-std').value = formatVND(data.financials.BS006);
            document.getElementById('eb-tl').value = formatVND(data.financials.BS007);
            document.getElementById('eb-equity').value = formatVND(data.financials.BS008);
            document.getElementById('eb-revenue').value = formatVND(data.financials.IS001);
            document.getElementById('eb-gp').value = formatVND(data.financials.IS002);
            document.getElementById('eb-ebit').value = formatVND(data.financials.IS003);
            document.getElementById('eb-interest').value = formatVND(data.financials.IS004);
            document.getElementById('eb-np').value = formatVND(data.financials.IS005);
            document.getElementById('eb-ocf').value = formatVND(data.financials.CF001);
            document.getElementById('eb-icf').value = formatVND(data.financials.CF002);
            document.getElementById('eb-fcf').value = formatVND(data.financials.CF003);
          }
        }
      } catch (err) {
        console.error(err);
      }
    }"""

if old_dead_script in html:
    html = html.replace(old_dead_script, "")
    print("Purged dead script block that caused DOM null errors")
else:
    print("old_dead_script not matched directly")

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html clean-up successfully!")
