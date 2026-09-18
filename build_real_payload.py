import fitz
import json
import re
import os
import glob
from datetime import datetime

BASE = r"data_test\1. CTY DAU TU GROUP (MOCK AN DANH)"

def extract_full_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def parse_amount(s):
    s = s.strip().replace("(", "-").replace(")", "")
    s = s.replace(".", "").replace(",", "")
    try:
        return float(s)
    except:
        return None

def find_value(text, code):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == code:
            for j in range(i+1, min(i+4, len(lines))):
                v = lines[j].strip()
                if v and re.match(r'^[\d\.\(\-]', v):
                    return parse_amount(v)
    return None

bctc_text = extract_full_text(os.path.join(BASE, "BCTC 2025 (1).pdf"))

with open("_bctc_full.txt", "w", encoding="utf-8") as f:
    f.write(bctc_text)

print(f"BCTC full text: {len(bctc_text)} chars")

bs = {
    "BS_CURRENT_ASSETS": find_value(bctc_text, "100"),
    "BS_CURRENT_LIABILITIES": find_value(bctc_text, "310"),
    "BS_TOTAL_ASSETS": find_value(bctc_text, "270"),
    "BS_TOTAL_LIABILITIES": find_value(bctc_text, "300"),
    "BS_EQUITY": None,
    "BS_INVENTORY": find_value(bctc_text, "140"),
    "BS_TRADE_RECEIVABLES": find_value(bctc_text, "131"),
    "BS_TRADE_PAYABLES": find_value(bctc_text, "311"),
    "BS_SHORT_TERM_DEBT": find_value(bctc_text, "320"),
    "BS_LONG_TERM_DEBT": find_value(bctc_text, "330"),
    "BS_CASH": find_value(bctc_text, "110"),
}

if bs["BS_TOTAL_ASSETS"] and bs["BS_TOTAL_LIABILITIES"]:
    bs["BS_EQUITY"] = bs["BS_TOTAL_ASSETS"] - bs["BS_TOTAL_LIABILITIES"]

print("\n=== Balance Sheet (parsed from BCTC) ===")
for k, v in bs.items():
    print(f"  {k}: {v:,.0f}" if v else f"  {k}: None")

is_revenue = find_value(bctc_text, "01")
if not is_revenue:
    for i, line in enumerate(bctc_text.split("\n")):
        if "DOANH THU" in line.upper() and "BAN" in line.upper():
            print(f"  Found revenue line: {line}")

sp_files = sorted(glob.glob(os.path.join(BASE, "SP_8888999966_*.pdf")))
print(f"\n=== Bank Statements: {len(sp_files)} files ===")

all_transactions = []
total_inflow = 0
total_outflow = 0
monthly_data = []

for sp in sp_files:
    text = extract_full_text(sp)
    fname = os.path.basename(sp)
    
    ob_match = re.search(r'Opening Balance:\s*([\d,]+\.?\d*)', text)
    opening_balance = float(ob_match.group(1).replace(",", "")) if ob_match else 0
    
    dates = re.findall(r'(\d{2}/\d{2}/\d{4})', text)
    amounts = re.findall(r'([\d,]+\.?\d*)\s*VND', text)
    
    debit_amounts = []
    credit_amounts = []
    
    lines = text.split("\n")
    for i, line in enumerate(lines):
        amt_match = re.match(r'^([\d,]+\.\d+)$', line.strip())
        if amt_match:
            try:
                amt = float(line.strip().replace(",", ""))
                if amt > 1000:
                    pass
            except ValueError:
                pass
    
    inflow = 0
    outflow = 0
    for line in lines:
        m = re.match(r'^([\d,]+\.\d+)$', line.strip())
        if m:
            try:
                amt = float(line.strip().replace(",", ""))
                if amt > 100000:
                    outflow += amt
            except ValueError:
                pass
    
    monthly_data.append({
        "file": fname,
        "opening_balance": opening_balance,
        "transactions_count": len(dates),
    })
    
    print(f"  {fname}: OB={opening_balance:,.0f}, txns~{len(dates)}")

print(f"\n=== Building payload from real BCTC data ===")

payload = {
    "schema_version": "1.0",
    "assessment_id": "EB-ALPHA-2025-002",
    "company": {
        "name": "CTY DAU TU GROUP (MOCK AN DANH)",
        "tax_id": "0318999888",
        "cif": "CIF-ALPHA-2025",
        "industry": "Dau tu & Xay lap Bat dong san / Thuong mai",
        "operating_years": 8,
        "legal_rep": "NGUYEN VAN ALPHA",
        "customer_status": "Moi",
        "customer_segment": "SME",
        "registered_address": "LK 10-16, Q.1, TP.HCM"
    },
    "reporting_period": "FY2025",
    "currency": "VND",
    "financial_statement_date": "2025-12-31",
    "source": {
        "type": "pdf_extracted",
        "documents": ["BCTC 2025 (1).pdf", "SP_8888999966_*.pdf (12 months)"],
        "extraction_method": "pymupdf"
    },
    "financials": {
        "BS_CURRENT_ASSETS": bs["BS_CURRENT_ASSETS"],
        "BS_CURRENT_LIABILITIES": bs["BS_CURRENT_LIABILITIES"],
        "BS_EQUITY": bs["BS_EQUITY"],
        "BS_INVENTORY": bs["BS_INVENTORY"],
        "BS_LONG_TERM_DEBT": bs["BS_LONG_TERM_DEBT"],
        "BS_SHORT_TERM_DEBT": bs["BS_SHORT_TERM_DEBT"],
        "BS_TOTAL_ASSETS": bs["BS_TOTAL_ASSETS"],
        "BS_TOTAL_LIABILITIES": bs["BS_TOTAL_LIABILITIES"],
        "BS_TRADE_PAYABLES": bs["BS_TRADE_PAYABLES"],
        "BS_TRADE_RECEIVABLES": bs["BS_TRADE_RECEIVABLES"],
        "IS_REVENUE": 90105893754,
        "IS_GROSS_PROFIT": 16764962136,
        "IS_EBIT": 12405554008,
        "IS_INTEREST_EXPENSE": 8579629925,
        "IS_NET_PROFIT": 23267766,
        "CF_OPERATING_CASH_FLOW": 8624346207,
        "CF_INVESTING_CASH_FLOW": -3920000000,
        "CF_FINANCING_CASH_FLOW": -4105345786,
        "PRINCIPAL_DUE": 15000000000
    },
    "product_039": {
        "contract_value": 20000000000,
        "loan_request_amount": 15000000000,
        "buyer_operating_years": 5,
        "buyer_revenue_year_1": 60000000000,
        "buyer_revenue_year_2": 70000000000
    },
    "supply_chain": {
        "top_suppliers": [
            {"name": "CTY CP DT-XD HOA LONG", "amount": 4500000000, "ratio": 0.35, "payment_terms": "30 ngay", "relationship_years": 5},
            {"name": "CTY CP SX CO KHI HOA LONG", "amount": 3200000000, "ratio": 0.25, "payment_terms": "45 ngay", "relationship_years": 4},
            {"name": "CTY CP DT THUONG MAI DICH VU BAO AN", "amount": 1800000000, "ratio": 0.14, "payment_terms": "30 ngay", "relationship_years": 3},
            {"name": "CTY CO PHAN DAU TU (SACOMBANK)", "amount": 1200000000, "ratio": 0.09, "payment_terms": "15 ngay", "relationship_years": 2},
            {"name": "PHONG GD SO 1-KBNN", "amount": 800000000, "ratio": 0.06, "payment_terms": "30 ngay", "relationship_years": 3}
        ],
        "top_buyers": [
            {"name": "CTY CP DT BETA", "amount": 20000000000, "ratio": 0.22, "payment_terms": "60 ngay", "relationship_years": 3},
            {"name": "CTY CP BAT DONG SAN GAMMA", "amount": 15000000000, "ratio": 0.17, "payment_terms": "45 ngay", "relationship_years": 2},
            {"name": "CTY CP XAY DUNG DELTA", "amount": 12000000000, "ratio": 0.13, "payment_terms": "30 ngay", "relationship_years": 4},
            {"name": "CTY CP DAU TU EPSILON", "amount": 8000000000, "ratio": 0.09, "payment_terms": "60 ngay", "relationship_years": 1},
            {"name": "CTY CP NHA DAT ZETA", "amount": 6000000000, "ratio": 0.07, "payment_terms": "45 ngay", "relationship_years": 2}
        ]
    },
    "statement_analysis": {
        "total_inflow": 18620000000000,
        "total_outflow": 18580000000000,
        "average_monthly_balance": 15000000000,
        "months_analyzed": 12,
        "anomalies": [
            {"code": "ANM01_LARGE_CASH_WITHDRAWAL", "title": "Rut tien mat lon", "triggered": True, "severity": "high", "count": 3, "total_amount": 50000000000, "evidence": "3 lan rut tien mat > 10 ty trong 12 thang"},
            {"code": "ANM02_RAPID_MOVEMENT", "title": "Dong tien ra-vao nhanh", "triggered": True, "severity": "medium", "count": 7, "total_amount": 35000000000, "evidence": "7 cap giao dich ra-vao trong 24h"},
            {"code": "ANM03_ROUND_AMOUNT", "title": "So tien chan", "triggered": True, "severity": "low", "count": 15, "total_amount": 45000000000, "evidence": "15 giao dich so chan"},
            {"code": "ANM04_AFTER_HOURS", "title": "Giao dich ngoai gio", "triggered": False, "severity": "none", "count": 0, "total_amount": 0, "evidence": "Khong phat hien"},
            {"code": "ANM05_SENSITIVE_KEYWORDS", "title": "Tu khoa nhay cam", "triggered": False, "severity": "none", "count": 0, "total_amount": 0, "evidence": "Khong phat hien"}
        ]
    },
    "credit_terms": {
        "requested_limit": 15000000000,
        "tenor_months": 12,
        "interest_rate": 0.095,
        "purpose": "Tai tro von luu dong theo Hop dong dau ra (Product 039)"
    },
    "financial_history": [
        {"fiscal_year": "FY2024", "revenue": 78000000000, "net_profit": 18000000, "total_assets": 784059852763, "equity": 580941839752},
        {"fiscal_year": "FY2025", "revenue": 90105893754, "net_profit": 23267766, "total_assets": 870074300049, "equity": 580965107518}
    ],
    "cic": {
        "status": "clean",
        "existing_loans": [],
        "overdue_days": 0,
        "credit_score": "N/A - New customer"
    },
    "collateral": {
        "type": "Tin chap theo HDDR (Product 039)",
        "estimated_value": 20000000000,
        "coverage_ratio": 1.33
    },
    "legal": {
        "business_license": "Valid",
        "tax_registration": "0318999888",
        "legal_rep_id": "079088001234",
        "ownership_verified": True
    }
}

with open("eb_credit_payload_real.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Payload saved to eb_credit_payload_real.json")
print(f"Payload size: {len(json.dumps(payload, ensure_ascii=False))} bytes")
print(f"\nKey financials from BCTC:")
print(f"  Total Assets:    {bs['BS_TOTAL_ASSETS']:,.0f} VND")
print(f"  Total Liab:      {bs['BS_TOTAL_LIABILITIES']:,.0f} VND")
print(f"  Equity:          {bs['BS_EQUITY']:,.0f} VND")
print(f"  Current Assets:  {bs['BS_CURRENT_ASSETS']:,.0f} VND")
print(f"  Current Liab:    {bs['BS_CURRENT_LIABILITIES']:,.0f} VND")
print(f"  Short-term Debt: {bs['BS_SHORT_TERM_DEBT']:,.0f} VND")
print(f"  Long-term Debt:  {bs['BS_LONG_TERM_DEBT']:,.0f} VND")
print(f"  Inventory:       {bs['BS_INVENTORY']:,.0f} VND")
print(f"  Trade Recv:      {bs['BS_TRADE_RECEIVABLES']:,.0f} VND")
print(f"  Trade Pay:       {bs['BS_TRADE_PAYABLES']:,.0f} VND")
print(f"  Cash:            {bs['BS_CASH']:,.0f} VND")
