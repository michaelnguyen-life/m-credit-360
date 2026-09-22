import io
import re

with io.open('server.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "company_match = re.search" in line and "cng ty" in line:
        lines[i] = "    company_match = re.search(r'(?:tên người nộp thuế|đơn vị báo cáo|đơn vị)[:\\\\s]*(công ty[^\\\\n]+)', text.lower())\n"
    elif "company_match = re.search" in line and "tn ng" in line:
        lines[i] = "    company_match = re.search(r'(?:tên người nộp thuế|đơn vị báo cáo|đơn vị)[:\\\\s]*(công ty[^\\\\n]+)', text.lower())\n"

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
