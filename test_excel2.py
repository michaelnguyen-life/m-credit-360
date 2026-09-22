import pandas as pd
import re
import unicodedata

file_path = r'C:\Users\finan\Downloads\BAO CAO TAI CHINH ALPHA GROUP 2025.xlsx'
try:
    all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
    text_parts = []
    for sn, df in all_sheets.items():
        for _, row in df.iterrows():
            vals = [str(v) for v in row if pd.notna(v) and str(v).strip()]
            if vals:
                text_parts.append(' '.join(vals))
    text = '\n'.join(text_parts)
    text_nfc = unicodedata.normalize('NFC', text)
    text_lower = text_nfc.lower()
    
    mst_match = re.search(r'(?:mã\s*số\s*thuế|mst|mã\s*số\s*doanh\s*nghiệp|tax\s*(?:code|id))[:\s\-]*([0-9]{10,14})', text_lower)
    if mst_match:
        print("MST:", mst_match.group(1))
    else:
        mst_match2 = re.search(r'\b([0-9]{10,14})\b', text_lower)
        print("MST fallback:", mst_match2.group(1) if mst_match2 else "None")
        print("Here are some 10-14 digit numbers found:")
        print(re.findall(r'\b([0-9]{10,14})\b', text_lower)[:10])

except Exception as e:
    print(f"Error: {e}")
