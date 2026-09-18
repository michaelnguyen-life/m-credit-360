import re
with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make search bar have an ID
content = content.replace('placeholder="Tìm kiếm khách hàng, mã hồ sơ..." class="w-56', 'id="global-search-input" placeholder="Tìm kiếm khách hàng, mã hồ sơ..." class="w-56')

search_logic = '''
    function setupSearch() {
        const input = document.getElementById('global-search-input');
        if (!input) return;
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const val = input.value.trim();
                if (val) {
                    showToast('Đang tìm kiếm: ' + val, 'info');
                    // Mock search load
                    setTimeout(() => {
                        document.getElementById('eb-tax-id').value = val;
                        document.getElementById('eb-company-name').value = "Khách hàng từ Search";
                        runEBAssessment();
                        input.value = '';
                    }, 500);
                }
            }
        });
    }
'''

content = content.replace('// Auto initialize on load', search_logic + '\n    // Auto initialize on load')
content = content.replace('setupSidebar();', 'setupSearch();\n      setupSidebar();')

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Search")
