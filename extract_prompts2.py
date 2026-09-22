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

output = "# Tổng hợp System Prompts & Templates các Agent (Phiên bản Code)\n\n"

for fp in files:
    if not os.path.exists(fp):
        output += f"## Error: Không tìm thấy file {os.path.basename(fp)}\n\n"
        continue
    
    with open(fp, 'r', encoding='utf-8') as f:
        src = f.read()
        
    output += f"## File: {os.path.basename(fp)}\n"
    count = 1
    
    class StringVisitor(ast.NodeVisitor):
        def __init__(self):
            self.strings = []
        
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                text = node.value.strip()
                if len(text) > 200:  # Prompts are usually long
                    self.strings.append(text)
            self.generic_visit(node)
            
        def visit_JoinedStr(self, node):
            # For f-strings, extract the raw text parts and join them loosely
            parts = []
            for v in node.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    parts.append(v.value)
                elif isinstance(v, ast.FormattedValue):
                    parts.append("{...}")
            text = "".join(parts).strip()
            if len(text) > 200:
                self.strings.append(text)
            self.generic_visit(node)
            
    try:
        tree = ast.parse(src)
        visitor = StringVisitor()
        visitor.visit(tree)
        
        for s in visitor.strings:
            output += f"### Đoạn Prompt/Template {count}\n`	ext\n{s}\n`\n\n"
            count += 1
            
        if count == 1:
            output += "*Không tìm thấy text dài nào > 200 ký tự.*\n\n"
    except Exception as e:
        output += f"*Lỗi phân tích cú pháp AST: {e}*\n\n"

with open('HANDOFF_PHUONG_PROMPTS.md', 'w', encoding='utf-8') as f:
    f.write(output)

print("Saved to HANDOFF_PHUONG_PROMPTS.md")
