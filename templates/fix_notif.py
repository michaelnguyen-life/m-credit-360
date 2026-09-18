import re
with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<button class="relative p-2 rounded-lg hover:bg-slate-100 text-[#667085] transition">', '<button onclick="openNotifications()" class="relative p-2 rounded-lg hover:bg-slate-100 text-[#667085] transition">')

notif_logic = '''
    function openNotifications() {
        showToast('Bạn có 3 thông báo mới chưa đọc', 'info');
        // Clear count
        const notifBadge = document.querySelector('button[onclick="openNotifications()"] span');
        if (notifBadge) {
            notifBadge.style.display = 'none';
        }
    }
'''

content = content.replace('// Auto initialize on load', notif_logic + '\n    // Auto initialize on load')

with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Notifications")
