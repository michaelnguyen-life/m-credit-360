import pandas as pd
import re
import unicodedata

file_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\04_QUAN_LY_KHACH_HANG\TEAM_TRIEU_DO_VIP\CTY NAM PHUONG XANH_TIN CHAP MSB\test\EXPORT_CHUAN_WEBSITE\BCTC_2025.xlsx'
all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
text_parts = []
for sn, df in all_sheets.items():
    for _, row in df.iterrows():
        vals = [str(v) for v in row if pd.notna(v) and str(v).strip()]
        if vals:
            text_parts.append(' '.join(vals))
text = '\n'.join(text_parts)

print('--- RAW TEXT EXTRACTED ---')
print(text[:1000])
print('--------------------------')

text = unicodedata.normalize('NFC', text)
for ch in range(1, 32):
    if ch != 10:
        text = text.replace(chr(ch), ' ')
text = text.lower()

keywords = {
    "IS_REVENUE": [r"doanh thu thuần", r"doanh thu bán hàng"],
    "IS_NET_PROFIT": [r"lợi nhuận sau thuế", r"lãi sau thuế"],
}

print('--- REGEX MATCHING ---')
for code, patterns in keywords.items():
    for pattern in patterns:
        m = re.search(pattern, text)
        print(f"[{code}] Pattern '{pattern}' matched: {m is not None}")

