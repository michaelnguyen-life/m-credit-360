import io
import re

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace extract_real_financials entirely
old_func = '''def extract_real_financials(text: str):
    keywords = {
        "IS_REVENUE": [r"doanh thu thuần", r"doanh thu bán hàng"],
        "IS_NET_PROFIT": [r"lợi nhuận sau thuế", r"lãi sau thuế"],
        "IS_INTEREST_EXPENSE": [r"chi phí lãi vay"],
        "BS_INVENTORY": [r"hàng tồn kho"],
        "BS_TRADE_RECEIVABLES": [r"phải thu ngắn hạn của khách hàng", r"phải thu khách hàng", r"phải thu ngắn hạn"],
        "BS_TRADE_PAYABLES": [r"phải trả người bán ngắn hạn", r"phải trả người bán"],
        "BS_SHORT_TERM_DEBT": [r"vay và nợ thuê tài chính ngắn hạn", r"vay ngắn hạn"],
        "BS_TOTAL_LIABILITIES": [r"nợ phải trả"],
        "BS_EQUITY": [r"vốn chủ sở hữu"],
        "CF_OPERATING_CASH_FLOW": [r"lưu chuyển tiền thuần từ hoạt động kinh doanh"],
        "BS_CURRENT_ASSETS": [r"tài sản ngắn hạn"],
        "BS_CURRENT_LIABILITIES": [r"nợ ngắn hạn"]
    }
    
    financials = {}
    # Fix weird pdf control characters
    for ch in range(1, 32):
        if ch != 10: # keep newline
            text = text.replace(chr(ch), ' ')
    lines = text.lower().split('\\n')
    
    for line in lines:
        for code, patterns in keywords.items():
            if code in financials:
                continue
            for pattern in patterns:
                if re.search(pattern, line):
                    numbers = re.findall(r'-?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?', line)
                    if numbers:
                        val = numbers[-1].replace(',', '').replace('.', '')
                        try:
                            financials[code] = int(val)
                        except:
                            pass
                    break
    
    # Fill defaults if missing to avoid breaking the form logic completely
    defaults = {
        "IS_REVENUE": 0, "IS_NET_PROFIT": 0, "IS_INTEREST_EXPENSE": 0,
        "BS_INVENTORY": 0, "BS_TRADE_RECEIVABLES": 0, "BS_TRADE_PAYABLES": 0,
        "BS_SHORT_TERM_DEBT": 0, "BS_TOTAL_LIABILITIES": 0, "BS_EQUITY": 0,
        "CF_OPERATING_CASH_FLOW": 0, "BS_CURRENT_ASSETS": 0, "BS_CURRENT_LIABILITIES": 0
    }
    for k, v in defaults.items():
        if k not in financials:
            financials[k] = v
            
    return financials'''

new_func = '''def extract_real_financials(text: str):
    keywords = {
        "IS_REVENUE": [r"doanh thu thuần", r"doanh thu bán hàng"],
        "IS_NET_PROFIT": [r"lợi nhuận sau thuế", r"lãi sau thuế"],
        "IS_INTEREST_EXPENSE": [r"chi phí lãi vay"],
        "BS_INVENTORY": [r"hàng tồn kho"],
        "BS_TRADE_RECEIVABLES": [r"phải thu của khách hàng", r"phải thu khách hàng", r"phải thu ngắn hạn"],
        "BS_TRADE_PAYABLES": [r"phải trả người bán ngắn hạn", r"phải trả người bán"],
        "BS_SHORT_TERM_DEBT": [r"vay và nợ thuê tài chính", r"vay ngắn hạn"],
        "BS_TOTAL_LIABILITIES": [r"nợ phải trả"],
        "BS_EQUITY": [r"vốn chủ sở hữu"],
        "CF_OPERATING_CASH_FLOW": [r"lưu chuyển tiền thuần từ hoạt động kinh doanh"],
        "BS_CURRENT_ASSETS": [r"tài sản ngắn hạn"],
        "BS_CURRENT_LIABILITIES": [r"nợ ngắn hạn"]
    }
    
    for ch in range(1, 32):
        if ch != 10:
            text = text.replace(chr(ch), ' ')
    text = text.lower()
    
    financials = {}
    for code, patterns in keywords.items():
        for pattern in patterns:
            match = re.search(pattern + r'.*?(\d{1,3}(?:\.\d{3})+)', text)
            if match:
                num_str = match.group(1).replace('.', '')
                try:
                    financials[code] = int(num_str)
                except:
                    pass
                break
    
    # Fill defaults if missing to avoid breaking the form logic completely
    defaults = {
        "IS_REVENUE": 0, "IS_NET_PROFIT": 0, "IS_INTEREST_EXPENSE": 0,
        "BS_INVENTORY": 0, "BS_TRADE_RECEIVABLES": 0, "BS_TRADE_PAYABLES": 0,
        "BS_SHORT_TERM_DEBT": 0, "BS_TOTAL_LIABILITIES": 0, "BS_EQUITY": 0,
        "CF_OPERATING_CASH_FLOW": 0, "BS_CURRENT_ASSETS": 0, "BS_CURRENT_LIABILITIES": 0
    }
    for k, v in defaults.items():
        if k not in financials:
            financials[k] = v
            
    return financials'''

code = code.replace(old_func, new_func)

# And fix MST logic
old_mst = '''mst_match = re.search(r'(?:Mã số doanh nghiệp|MST)[:\s-]*(\d{10,14})', text, re.IGNORECASE)
    if mst_match:
        mst = mst_match.group(1)'''

new_mst = '''mst_match = re.search(r'mã số thuế.*?(0\d{9})', text.lower())
    if mst_match:
        mst = mst_match.group(1)
    else:
        mst_match = re.search(r'(?:mã số doanh nghiệp|mst)[:\s-]*(\d{10,14})', text.lower())
        if mst_match:
            mst = mst_match.group(1)'''

code = code.replace(old_mst, new_mst)

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
