import re

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I will append new mock data right after EMBEDDED_RB_DATA

new_data = '''
# --- 4 EB SCENARIOS ---
EB_GOOD_1 = EMBEDDED_KHANGTHINH_DATA

EB_GOOD_2 = {
  "assessment_id": "EB-VINAMILK-2025",
  "company": {
    "tax_id": "0300588569",
    "name": "CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)",
    "industry": "FMCG - Thực phẩm",
    "operating_years": 45,
    "legal_rep": "MAI KIỀU LIÊN"
  },
  "reporting_period": "2025",
  "currency": "VND",
  "financials": {
    "BS_CURRENT_ASSETS": 35000000000000,
    "BS_CURRENT_LIABILITIES": 15000000000000,
    "BS_TRADE_RECEIVABLES": 6000000000000,
    "BS_INVENTORY": 7000000000000,
    "BS_TRADE_PAYABLES": 5000000000000,
    "BS_SHORT_TERM_DEBT": 8000000000000,
    "BS_TOTAL_LIABILITIES": 17000000000000,
    "BS_EQUITY": 34000000000000,
    "IS_REVENUE": 60000000000000,
    "IS_GROSS_PROFIT": 25000000000000,
    "IS_EBIT": 12000000000000,
    "IS_INTEREST_EXPENSE": 500000000000,
    "IS_NET_PROFIT": 9000000000000,
    "CF_OPERATING_CASH_FLOW": 11000000000000,
    "CF_INVESTING_CASH_FLOW": -3000000000000,
    "CF_FINANCING_CASH_FLOW": -5000000000000,
    "PRINCIPAL_DUE": 3000000000000
  },
  "dsp": {
    "revenue": 60000000000000,
    "trade_receivables": 6000000000000
  },
  "product_039": {
    "customer_operating_years": 45,
    "customer_equity": 34000000000000,
    "buyer_name": "HỆ THỐNG SIÊU THỊ COOPMART",
    "buyer_operating_years": 25,
    "buyer_avg_revenue_2y": 40000000000000,
    "contract_value": 5000000000000,
    "loan_request_amount": 2000000000000
  }
}

EB_BAD_1 = EMBEDDED_FLC_DATA

EB_BAD_2 = {
  "assessment_id": "EB-THM-2023",
  "company": {
    "tax_id": "0101010101",
    "name": "TẬP ĐOÀN TÂN HOÀNG MINH",
    "industry": "Bất động sản",
    "operating_years": 20,
    "legal_rep": "ĐỖ ANH DŨNG"
  },
  "reporting_period": "2023",
  "currency": "VND",
  "financials": {
    "BS_CURRENT_ASSETS": 25000000000000,
    "BS_CURRENT_LIABILITIES": 45000000000000,
    "BS_TRADE_RECEIVABLES": 12000000000000,
    "BS_INVENTORY": 15000000000000,
    "BS_TRADE_PAYABLES": 5000000000000,
    "BS_SHORT_TERM_DEBT": 35000000000000,
    "BS_TOTAL_LIABILITIES": 50000000000000,
    "BS_EQUITY": -5000000000000,
    "IS_REVENUE": 1500000000000,
    "IS_GROSS_PROFIT": 100000000000,
    "IS_EBIT": -1200000000000,
    "IS_INTEREST_EXPENSE": 2500000000000,
    "IS_NET_PROFIT": -3500000000000,
    "CF_OPERATING_CASH_FLOW": -4000000000000,
    "CF_INVESTING_CASH_FLOW": -1000000000000,
    "CF_FINANCING_CASH_FLOW": 6000000000000,
    "PRINCIPAL_DUE": 15000000000000
  },
  "dsp": {
    "revenue": 50000000000,
    "trade_receivables": 12000000000000
  },
  "product_039": {
    "customer_operating_years": 20,
    "customer_equity": -5000000000000,
    "buyer_name": "CTCP ĐẦU TƯ ẢO",
    "buyer_operating_years": 1,
    "buyer_avg_revenue_2y": 0,
    "contract_value": 5000000000000,
    "loan_request_amount": 4000000000000
  }
}

# --- 4 RB SCENARIOS ---
RB_GOOD_1 = EMBEDDED_RB_DATA

RB_GOOD_2 = {
  "assessment_id": "RB-SHOPEE-002",
  "data_classification": "SYNTHETIC",
  "customer": {
    "customer_id": "KH02",
    "name": "NGUYỄN VĂN TỐT",
    "segment": "individual_business_owner",
    "business_channel": "Shopee Mall",
    "business_tenure_months": 36
  },
  "income": [
    {
      "type": "business",
      "monthly_amount": 4500000000,
      "verification_status": "verified",
      "eligible_percent": 0.10,
      "source": "Shopee API"
    }
  ],
  "existing_debts": [],
  "credit_cards": [],
  "loan": {
    "product": "unsecured_working_capital_demo",
    "amount": 800000000,
    "annual_interest_rate": 0.18,
    "tenor_months": 24,
    "secured": false,
    "purpose": "Nhập hàng mùa Tết"
  },
  "documents": {
    "identity": True,
    "income_proof": True,
    "cic": True,
    "business_registration": True,
    "platform_evidence": True
  },
  "rules": {
    "max_dti": 0.55,
    "min_disposable_income": 5000000,
    "max_card_utilization": 0.8,
    "max_unverified_income_share": 0.35
  }
}

RB_BAD_1 = {
  "assessment_id": "RB-FB-003",
  "data_classification": "SYNTHETIC",
  "customer": {
    "customer_id": "KH03",
    "name": "LÊ THỊ ĐỎ",
    "segment": "individual_business_owner",
    "business_channel": "Livestream Facebook",
    "business_tenure_months": 12
  },
  "income": [
    {
      "type": "business",
      "monthly_amount": 1500000000,
      "verification_status": "unverified",
      "eligible_percent": 0.05,
      "source": "Sổ tay cá nhân"
    }
  ],
  "existing_debts": [
    {
      "type": "unsecured_loan",
      "outstanding": 500000000,
      "monthly_payment": 25000000
    }
  ],
  "credit_cards": [
    {
      "limit": 100000000,
      "balance": 95000000
    }
  ],
  "loan": {
    "product": "unsecured_working_capital_demo",
    "amount": 500000000,
    "annual_interest_rate": 0.25,
    "tenor_months": 36,
    "secured": false,
    "purpose": "Gồng lỗ chi phí quảng cáo"
  },
  "documents": {
    "identity": True,
    "income_proof": False,
    "cic": True,
    "business_registration": False,
    "platform_evidence": False
  },
  "rules": {
    "max_dti": 0.55,
    "min_disposable_income": 5000000,
    "max_card_utilization": 0.8,
    "max_unverified_income_share": 0.35
  }
}

RB_BAD_2 = {
  "assessment_id": "RB-SHOPEE-004",
  "data_classification": "SYNTHETIC",
  "customer": {
    "customer_id": "KH04",
    "name": "TRẦN VĂN TRỄ",
    "segment": "individual_business_owner",
    "business_channel": "Shopee Dropship",
    "business_tenure_months": 6
  },
  "income": [
    {
      "type": "business",
      "monthly_amount": 20000000,
      "verification_status": "verified",
      "eligible_percent": 0.15,
      "source": "Shopee API"
    }
  ],
  "existing_debts": [
    {
      "type": "short_term_loan",
      "outstanding": 150000000,
      "monthly_payment": 15000000
    }
  ],
  "credit_cards": [],
  "loan": {
    "product": "unsecured_working_capital_demo",
    "amount": 200000000,
    "annual_interest_rate": 0.22,
    "tenor_months": 12,
    "secured": false,
    "purpose": "Vay đảo nợ"
  },
  "documents": {
    "identity": True,
    "income_proof": True,
    "cic": True,
    "business_registration": False,
    "platform_evidence": True
  },
  "rules": {
    "max_dti": 0.55,
    "min_disposable_income": 5000000,
    "max_card_utilization": 0.8,
    "max_unverified_income_share": 0.35
  }
}
'''

content = content.replace("EMBEDDED_RB_DATA = json.loads", new_data + "\nEMBEDDED_RB_DATA_OLD = json.loads")

# Update get_sample_eb logic
new_eb_logic = '''
    sid = sample_id.lower()
    if sid == 'eb_good_1' or sid == 'khangthinh': return EB_GOOD_1
    if sid == 'eb_good_2' or sid == 'vinamilk': return EB_GOOD_2
    if sid == 'eb_bad_1' or sid == 'flc': return EB_BAD_1
    if sid == 'eb_bad_2' or sid == 'tanhoangminh': return EB_BAD_2
    
    if sid == 'beta':
'''
content = content.replace("if sample_id.lower() == 'khangthinh':\n        return EMBEDDED_KHANGTHINH_DATA\n    elif sample_id.lower() == 'flc':\n        return EMBEDDED_FLC_DATA\n    elif sample_id.lower() == 'beta':", new_eb_logic)

# Update get_sample_rb logic
new_rb_logic = '''
def get_sample_rb(sample_id: str):
    sid = sample_id.lower()
    if sid == 'rb_good_1': return RB_GOOD_1
    if sid == 'rb_good_2': return RB_GOOD_2
    if sid == 'rb_bad_1': return RB_BAD_1
    if sid == 'rb_bad_2': return RB_BAD_2

    if os.path.exists(SAMPLE_RB_PATH):
'''
content = content.replace("def get_sample_rb(sample_id: str):\n    if os.path.exists(SAMPLE_RB_PATH):", new_rb_logic)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched server.py successfully!")
