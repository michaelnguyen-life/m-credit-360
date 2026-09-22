import os, shutil

src_root = r"C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\M_CREDIT_360"
dst_root = r"C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\NOP BAI\M_CREDIT_360_FINAL_ALL_IN_ONE"

shutil.copy2(os.path.join(src_root, "templates/index.html"), os.path.join(dst_root, "templates/index.html"))
print("Synced clean index.html to NOP BAI")
