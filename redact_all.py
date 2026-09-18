import os
import shutil
import pymupdf
import openpyxl
import re

src_dir = r"C:\Users\finan\OneDrive\Desktop\KHANG THINH - KHOA"
dst_dir = r"C:\Users\finan\OneDrive\Desktop\KHANG THINH - KHOA (REDACTED)"

if os.path.exists(dst_dir):
    shutil.rmtree(dst_dir)
os.makedirs(dst_dir)

redact_words = [
    "KHANG THỊNH", "KHANG THINH", "KHOA", "0305956840", 
    "Hải", "Nhung", "Lộc Khánh", "Lộc Thịnh",
    "AGRIBANK", "Agribank", "Thành Đô", "622320"
]

def redact_pdf(src, dst):
    try:
        doc = pymupdf.open(src)
        for page in doc:
            for word in redact_words:
                areas = page.search_for(word)
                for area in areas:
                    page.add_redact_annot(area, fill=(0, 0, 0))
            page.apply_redactions()
        doc.save(dst)
        return True
    except Exception as e:
        print(f"Error PDF {src}: {e}")
        return False

def redact_xlsx(src, dst):
    try:
        wb = openpyxl.load_workbook(src)
        for sheet in wb.worksheets:
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.value and isinstance(cell.value, str):
                        val = cell.value
                        changed = False
                        for w in redact_words:
                            if w.lower() in val.lower():
                                val = re.sub(w, "[REDACTED]", val, flags=re.IGNORECASE)
                                changed = True
                        if changed:
                            cell.value = val
        wb.save(dst)
        return True
    except Exception as e:
        print(f"Error XLSX {src}: {e}")
        return False

for root, dirs, files in os.walk(src_dir):
    rel_path = os.path.relpath(root, src_dir)
    target_root = os.path.join(dst_dir, rel_path)
    os.makedirs(target_root, exist_ok=True)
    
    for f in files:
        src_file = os.path.join(root, f)
        
        # redact filenames too
        new_f = f
        for w in redact_words:
            new_f = re.sub(w, "REDACTED", new_f, flags=re.IGNORECASE)
        dst_file = os.path.join(target_root, new_f)
        
        ext = f.lower().split('.')[-1]
        
        if ext == 'pdf':
            success = redact_pdf(src_file, dst_file)
            if not success: shutil.copy2(src_file, dst_file)
        elif ext == 'xlsx':
            success = redact_xlsx(src_file, dst_file)
            if not success: shutil.copy2(src_file, dst_file)
        else:
            shutil.copy2(src_file, dst_file)

print("Redaction completed in:", dst_dir)
