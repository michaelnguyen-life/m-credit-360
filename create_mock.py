import os
import shutil
import json

src_dir = r"C:\Users\finan\OneDrive\Desktop\KHANG THINH - KHOA"
dst_dir = r"C:\Users\finan\OneDrive\Desktop\KHANG THINH - KHOA (MOCK)"

if os.path.exists(dst_dir):
    shutil.rmtree(dst_dir)
os.makedirs(dst_dir)

# Create identical folder structure with mock files
for root, dirs, files in os.walk(src_dir):
    rel_path = os.path.relpath(root, src_dir)
    target_root = os.path.join(dst_dir, rel_path)
    os.makedirs(target_root, exist_ok=True)
    
    for f in files:
        # Just create an empty file with the same name
        with open(os.path.join(target_root, f), 'w', encoding='utf-8') as fw:
            fw.write("This is a mock file for testing M-CREDIT 360 AI.")

# Create the payload JSON
payload = {
    "assessment_id": "EB-KHANGTHINH-2026",
    "company": {
        "tax_id": "0305956840",
        "name": "CÔNG TY TNHH XD - TTNT KHANG THỊNH"
    },
    "financials": {
        "IS_REVENUE": 20278122298,
        "IS_EBIT": 34825664,
        "BS_CURRENT_ASSETS": 25818411666,
        "BS_CURRENT_LIABILITIES": 20534512914,
        "BS_TRADE_RECEIVABLES": 11161376091, 
        "BS_INVENTORY": 11161376091, 
        "BS_TRADE_PAYABLES": 11000000000,
        "BS_EQUITY": 5283898752,
        "IS_INTEREST_EXPENSE": 1204261813
    },
    "debt_service": {
        "principal_due": 3000000000
    },
    "product_039": {
        "contract_value": 15000000000,
        "loan_request_amount": 10000000000,
        "customer_equity": 5283898752
    }
}

with open(os.path.join(dst_dir, "eb_credit_payload_khang_thinh.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=4, ensure_ascii=False)

print("Mock folder created successfully at:", dst_dir)
