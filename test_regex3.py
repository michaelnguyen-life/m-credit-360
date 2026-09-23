from server import extract_real_financials
import pandas as pd

file_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\04_QUAN_LY_KHACH_HANG\TEAM_TRIEU_DO_VIP\CTY NAM PHUONG XANH_TIN CHAP MSB\test\EXPORT_CHUAN_WEBSITE\BCTC_2025.xlsx'
all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
text_parts = []
for sn, df in all_sheets.items():
    for _, row in df.iterrows():
        vals = [str(v) for v in row if pd.notna(v) and str(v).strip()]
        if vals:
            text_parts.append(' '.join(vals))
text = '\n'.join(text_parts)

fin = extract_real_financials(text)
print('--- EXTRACTED FROM BCTC_2025.xlsx ---')
for k, v in fin.items():
    print(k, v)

file_path2 = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\04_QUAN_LY_KHACH_HANG\TEAM_TRIEU_DO_VIP\CTY NAM PHUONG XANH_TIN CHAP MSB\test\EXPORT_CHUAN_WEBSITE\BCTC_MSB_CODES.xlsx'
all_sheets2 = pd.read_excel(file_path2, sheet_name=None, header=None)
text_parts2 = []
for sn, df in all_sheets2.items():
    for _, row in df.iterrows():
        vals = [str(v) for v in row if pd.notna(v) and str(v).strip()]
        if vals:
            text_parts2.append(' '.join(vals))
text2 = '\n'.join(text_parts2)

fin2 = extract_real_financials(text2)
print('\n--- EXTRACTED FROM BCTC_MSB_CODES.xlsx ---')
for k, v in fin2.items():
    print(k, v)
