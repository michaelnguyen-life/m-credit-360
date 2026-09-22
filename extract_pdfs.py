import fitz
import json
import os
import glob

base = r"data_test\1. CTY DAU TU GROUP (MOCK AN DANH)"

files = {
    "BCTC_2025": os.path.join(base, "BCTC 2025 (1).pdf"),
    "FGC_chi_tiet": os.path.join(base, "FGC.Chi tiết các TK 2025.pdf"),
    "GCN": os.path.join(base, "GCN - NGUYEN VAN ALPHA.pdf"),
    "CCCD": os.path.join(base, "1.CCCD NGUYEN VAN ALPHA.pdf"),
}

sp_files = sorted(glob.glob(os.path.join(base, "SP_8888999966_*.pdf")))

results = {}

for name, path in files.items():
    if os.path.exists(path):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        results[name] = {
            "file": os.path.basename(path),
            "pages": len(fitz.open(path)),
            "chars": len(text),
            "text": text[:5000]
        }
        print(f"[OK] {name}: {os.path.basename(path)} - {len(text)} chars")
    else:
        print(f"[SKIP] {name}: not found")

print(f"\n--- Sao ke files: {len(sp_files)} ---")
sp_results = []
for sp in sp_files:
    doc = fitz.open(sp)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    sp_results.append({
        "file": os.path.basename(sp),
        "chars": len(text),
        "text": text[:3000]
    })
    print(f"  [OK] {os.path.basename(sp)}: {len(text)} chars")

results["sao_ke_list"] = sp_results

with open("extracted_pdfs.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nSaved to extracted_pdfs.json ({len(json.dumps(results, ensure_ascii=False))} bytes)")
