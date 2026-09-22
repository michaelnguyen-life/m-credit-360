import os, shutil

src_root = r"C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M_CREDIT_360"
dst_root = r"C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\NOP BAI\M_CREDIT_360_FINAL_ALL_IN_ONE"

# Files to copy directly
files_to_sync = [
    "server.py",
    "requirements.txt",
    "Dockerfile",
    "templates/index.html",
    "agents/rb_credit_memo_builder.py",
    "agents/eb_credit_agent.py",
    "agents/retail_credit_agent.py",
    "agents/credit_memo_builder_agent.py",
    "static/img/m_insight_logo.png"
]

for rel_path in files_to_sync:
    src = os.path.join(src_root, rel_path)
    dst = os.path.join(dst_root, rel_path)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Synced: {rel_path} -> OK")
    else:
        print(f"Source not found: {rel_path}")

# Copy template MB01A if exists
mb01a_src = r"C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx"
mb01a_dst = os.path.join(dst_root, "MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx")
if os.path.exists(mb01a_src):
    shutil.copy2(mb01a_src, mb01a_dst)
    print("Synced MB01A template to NOP BAI root -> OK")

print("All key files synced to NOP BAI successfully!")
