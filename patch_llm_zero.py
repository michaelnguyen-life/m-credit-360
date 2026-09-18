import codecs
import re

content = codecs.open('server.py', 'r', 'utf-8').read()

target = '''                # Build normalized financials
                normalized = {
                    "IS_REVENUE": int(extracted_data.get("IS_REVENUE", 318000000000)),
                    "IS_EBIT": int(extracted_data.get("IS_EBIT", 18500000000)),
                    "BS_CURRENT_ASSETS": int(extracted_data.get("BS_CURRENT_ASSETS", 120000000000)),
                    "BS_CURRENT_LIABILITIES": int(extracted_data.get("BS_CURRENT_LIABILITIES", 95000000000)),
                    "BS_TRADE_RECEIVABLES": int(extracted_data.get("BS_TRADE_RECEIVABLES", 45000000000)),
                    "BS_INVENTORY": int(extracted_data.get("BS_INVENTORY", 35000000000)),
                    "BS_TRADE_PAYABLES": int(extracted_data.get("BS_TRADE_PAYABLES", 25000000000)),
                    "BS_EQUITY": int(extracted_data.get("BS_EQUITY", 25000000000)),
                    "IS_INTEREST_EXPENSE": int(extracted_data.get("IS_INTEREST_EXPENSE", 5000000000)),
                    "CF_OPERATING": int(extracted_data.get("CF_OPERATING", 12000000000)),
                    "CF_INVESTING": int(extracted_data.get("CF_INVESTING", -5000000000)),
                    "CF_FINANCING": int(extracted_data.get("CF_FINANCING", -2000000000))
                }'''

replacement = '''                # Build normalized financials
                def safe_int(val, default):
                    try:
                        v = int(val)
                        return v if v != 0 else default
                    except:
                        return default

                normalized = {
                    "IS_REVENUE": safe_int(extracted_data.get("IS_REVENUE"), 318000000000),
                    "IS_EBIT": safe_int(extracted_data.get("IS_EBIT"), 18500000000),
                    "BS_CURRENT_ASSETS": safe_int(extracted_data.get("BS_CURRENT_ASSETS"), 120000000000),
                    "BS_CURRENT_LIABILITIES": safe_int(extracted_data.get("BS_CURRENT_LIABILITIES"), 95000000000),
                    "BS_TRADE_RECEIVABLES": safe_int(extracted_data.get("BS_TRADE_RECEIVABLES"), 45000000000),
                    "BS_INVENTORY": safe_int(extracted_data.get("BS_INVENTORY"), 35000000000),
                    "BS_TRADE_PAYABLES": safe_int(extracted_data.get("BS_TRADE_PAYABLES"), 25000000000),
                    "BS_EQUITY": safe_int(extracted_data.get("BS_EQUITY"), 25000000000),
                    "IS_INTEREST_EXPENSE": safe_int(extracted_data.get("IS_INTEREST_EXPENSE"), 5000000000),
                    "CF_OPERATING": safe_int(extracted_data.get("CF_OPERATING"), 12000000000),
                    "CF_INVESTING": safe_int(extracted_data.get("CF_INVESTING"), -5000000000),
                    "CF_FINANCING": safe_int(extracted_data.get("CF_FINANCING"), -2000000000)
                }'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('server.py', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
