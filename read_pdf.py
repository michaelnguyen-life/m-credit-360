import os
import pymupdf
base_dir = r"C:\Users\finan\OneDrive\Desktop\KHANG THINH - KHOA"
tc_dir = [d for d in os.listdir(base_dir) if 'ch' in d.lower()][0]
tc_path = os.path.join(base_dir, tc_dir)
bctc_file = [f for f in os.listdir(tc_path) if '2025' in f and f.lower().endswith('.pdf')][0]

doc = pymupdf.open(os.path.join(tc_path, bctc_file))
text = ""
for page in doc:
    text += page.get_text()
with open('bctc.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Extracted", len(text), "chars")
