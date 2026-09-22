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
    
    with open('test_out.txt', 'w', encoding='utf-8') as f:
        f.write("TEXT SNIPPET:\n")
        f.write(text[:1000] + "\n")
        
        text_nfc = unicodedata.normalize('NFC', text)
        text_lower = text_nfc.lower()
        
        f.write("\n--- MATCHING ---\n")
        company_match = re.search(r'(công ty\s+(?:tnhh|cp|cổ phần|trách nhiệm|tập đoàn)[a-zà-ỹ\s]{3,60})', text_lower)
        f.write("Company: " + (company_match.group(1) if company_match else "None") + "\n")
        
        mst_match = re.search(r'(?:mã\s*số\s*thuế|mst|mã\s*số\s*doanh\s*nghiệp|tax\s*(?:code|id))[:\s\-]*([0-9]{10,14})', text_lower)
        f.write("MST: " + (mst_match.group(1) if mst_match else "None") + "\n")
        
        period_match = re.search(r'(?:năm|kỳ báo cáo|năm tài chính)[:\s-]*([12]\d{3})', text_lower)
        if not period_match:
            period_match = re.search(r'\b(202[0-9])\b', text_lower)
        f.write("Period: " + (period_match.group(1) if period_match else "None") + "\n")

except Exception as e:
    with open('test_out.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}")
