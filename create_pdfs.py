import pymupdf
import os

demo_dir = r"C:\Users\finan\OneDrive\Desktop\MOCK_PDFs_FOR_DEMO"
os.makedirs(demo_dir, exist_ok=True)

files = [
    ("BCTC_2025_KhangThinh_SME.pdf", "Ho so BCTC - Cong ty Khang Thinh (Mock)"),
    ("BCTC_2025_Vinamilk_Corp.pdf", "Ho so BCTC - Cong ty Vinamilk (Mock)"),
    ("BCTC_2022_FLC_Group.pdf", "Ho so BCTC - Tap doan FLC (Mock)"),
    ("BCTC_2023_TanHoangMinh.pdf", "Ho so BCTC - Tap doan Tan Hoang Minh (Mock)")
]

for filename, text in files:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), text, fontsize=14)
    page.insert_text((50, 80), "File duoc tao boi Omni-Butler de test giao dien Upload.", fontsize=10)
    doc.save(os.path.join(demo_dir, filename))

print("Created PDF files at:", demo_dir)
