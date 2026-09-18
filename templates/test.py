with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
match = re.search(r'function saveDraftNotification.*?\}', content, re.DOTALL)
if match:
    with open('test_out.txt', 'w', encoding='utf-8') as fw:
        fw.write(match.group(0))
