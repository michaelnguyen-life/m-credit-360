import os
import pymupdf

base_dir = r"C:\Users\finan\OneDrive\Desktop\KHANG THINH - KHOA"
tc_dir = [d for d in os.listdir(base_dir) if 'ch' in d.lower()][0]
tc_path = os.path.join(base_dir, tc_dir)
bctc_file = [f for f in os.listdir(tc_path) if '2025' in f and f.lower().endswith('.pdf')][0]
src_pdf = os.path.join(tc_path, bctc_file)
dst_pdf = "test_redacted.pdf"

try:
    doc = pymupdf.open(src_pdf)
    redact_words = ["KHANG THỊNH", "KHANG THINH", "KHOA", "0305956840"]
    count = 0
    for page in doc:
        for word in redact_words:
            # search ignores case by default in some versions, but let's be explicit if possible
            # PyMuPDF search_for is case sensitive by default, so we'll add lower/upper variations
            pass
            
    # better approach: just search for these exact strings
    for page in doc:
        for word in redact_words:
            areas = page.search_for(word)
            for area in areas:
                page.add_redact_annot(area, fill=(0, 0, 0)) # black out
                count += 1
        page.apply_redactions()
    
    doc.save(dst_pdf)
    print(f"Redacted {count} occurrences in PDF.")
except Exception as e:
    print("Error:", e)
