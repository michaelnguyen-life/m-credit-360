import re

def extract_real_financials(text: str):
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
    lines = text.lower().split('\n')
    
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
    
    return financials

text = """Doanh thu thuần về bán hàng và cung cấp dịch vụ (10= 01-02)1020.278.122.29823.157.909.231"""
print(extract_real_financials(text))
