import ast
import os

files = [
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\agents\eb_credit_agent.py',
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\agents\retail_credit_agent.py',
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\agents\credit_memo_builder_agent.py',
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\agents\statement_analyzer_agent.py',
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\agents\policy_eligibility_agent.py',
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\agents\rb_credit_memo_builder.py',
    r'c:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M-Insight360\server.py'
]

output = "# Tổng hợp System Prompts & Templates các Agent\n\n"

for fp in files:
    if not os.path.exists(fp):
        output += f"## Error: Không tìm thấy file {os.path.basename(fp)}\n\n"
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        src = f.read()
    
    # Simple regex to catch triple quoted strings
    import re
    # Match both ''' and """
    matches = re.finditer(r'r?\"\"\"(.*?)\"\"\"|r?\'\'\'(.*?)\'\'\'', src, re.DOTALL)
    
    output += f"## File: {os.path.basename(fp)}\n"
    count = 1
    for m in matches:
        text = m.group(1) if m.group(1) is not None else m.group(2)
        if len(text.strip()) > 50 and ('Bạn là' in text or 'prompt' in text.lower() or 'hệ thống' in text.lower() or 'tờ trình' in text.lower() or 'system' in text.lower()):
            output += f"### Prompt {count}\n`	ext\n{text.strip()}\n`\n\n"
            count += 1
    
    if count == 1:
        output += "*Không tìm thấy prompt dạng triple-quote dài*\n\n"

with open('HANDOFF_PHUONG_PROMPTS.md', 'w', encoding='utf-8') as f:
    f.write(output)

print("Saved to HANDOFF_PHUONG_PROMPTS.md")
