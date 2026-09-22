import io
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
    for ch in range(1, 32):
        if ch != 10:
            text = text.replace(chr(ch), ' ')
    lines = text.lower().split('\n')
    
    for line in lines:
        for code, patterns in keywords.items():
            if code in financials:
                continue
            for pattern in patterns:
                if re.search(pattern, line):
                    numbers = re.findall(r'-?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?', line)
                    if numbers:
                        # Extract the FIRST number after the keyword?
                        # Or the LARGEST number?
                        # Usually BCTC has Code, This Year, Last Year
                        # Example: 10 20.278.122.298 23.157.909.231
                        # If we pick the SECOND to last, it might be This Year.
                        # Wait, what if there's no Code?
                        
                        # Let's just pick the FIRST valid large number (>1000)
                        val = 0
                        for num in numbers:
                            clean_num = num.replace(',', '').replace('.', '')
                            try:
                                n = int(clean_num)
                                if n > 1000 or n < -1000:
                                    val = n
                                    break
                            except:
                                pass
                        
                        financials[code] = val
                    break
    
    return financials

from pypdf import PdfReader
reader = PdfReader('data_test/BCTC 2025 ĐK.pdf')
text = ""
for page in reader.pages:
    text += (page.extract_text() or "") + "\n"

print(extract_real_financials(text))
