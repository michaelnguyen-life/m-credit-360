import re

with open('server.py', 'r', encoding='utf-8') as f:
    server_content = f.read()

# Add KHANG THINH data
khangthinh_data = '''
EMBEDDED_KHANGTHINH_DATA = {
  "assessment_id": "EB-KHANGTHINH-2026",
  "company": {
    "tax_id": "0305956840",
    "name": "CÔNG TY TNHH XD - TTNT KHANG THỊNH",
    "industry": "Xây dựng & Kiến trúc",
    "operating_years": 10,
    "legal_rep": "NGUYỄN VĂN MOCK"
  },
  "reporting_period": "2025",
  "currency": "VND",
  "financials": {
    "BS_CURRENT_ASSETS": 25818411666,
    "BS_CURRENT_LIABILITIES": 20534512914,
    "BS_TRADE_RECEIVABLES": 11161376091,
    "BS_INVENTORY": 11161376091,
    "BS_TRADE_PAYABLES": 11000000000,
    "BS_SHORT_TERM_DEBT": 15000000000,
    "BS_TOTAL_LIABILITIES": 20534512914,
    "BS_EQUITY": 5283898752,
    "IS_REVENUE": 20278122298,
    "IS_GROSS_PROFIT": 2928935485,
    "IS_EBIT": 34825664,
    "IS_INTEREST_EXPENSE": 1204261813,
    "IS_NET_PROFIT": 20009642,
    "CF_OPERATING_CASH_FLOW": 1448157955,
    "CF_INVESTING_CASH_FLOW": -19147085,
    "CF_FINANCING_CASH_FLOW": -19373124229,
    "PRINCIPAL_DUE": 3000000000
  },
  "dsp": {
    "revenue": 20278122298,
    "trade_receivables": 11161376091
  },
  "product_039": {
    "customer_operating_years": 10,
    "customer_equity": 5283898752,
    "buyer_name": "BAN QLDA ĐTXD",
    "buyer_operating_years": 5,
    "buyer_avg_revenue_2y": 50000000000,
    "contract_value": 15000000000,
    "loan_request_amount": 10000000000
  }
}
'''

if 'EMBEDDED_KHANGTHINH_DATA' not in server_content:
    server_content = server_content.replace('EMBEDDED_RB_DATA = json.loads', khangthinh_data + '\nEMBEDDED_RB_DATA = json.loads')

    # Update get_sample_eb logic
    new_logic = '''
    if sample_id.lower() == 'khangthinh':
        return EMBEDDED_KHANGTHINH_DATA
    elif sample_id.lower() == 'beta':
'''
    server_content = server_content.replace("if sample_id.lower() == 'beta':", new_logic)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server_content)
print("Updated server.py")
