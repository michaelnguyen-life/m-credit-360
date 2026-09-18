with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
if 'onchange=\"handleFileSelect(event)\"' not in content:
    content = content.replace('<input id=\"file-input\" type=\"file\" multiple class=\"hidden\" />', '<input id=\"file-input\" type=\"file\" multiple class=\"hidden\" onchange=\"handleFileSelect(event)\" accept=\".pdf,.docx,.xlsx,.xls,.csv,.jpg,.png,.zip\" />')
    with open('c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE/templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated input")
else:
    print("Already updated")
