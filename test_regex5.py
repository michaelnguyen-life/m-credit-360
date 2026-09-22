import io
import re
from pypdf import PdfReader

reader = PdfReader('data_test/BCTC 2025 ĐK.pdf')
text = ""
for page in reader.pages:
    text += (page.extract_text() or "") + " "

for ch in range(1, 32):
    if ch != 10:
        text = text.replace(chr(ch), ' ')
text = text.lower()

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

financials = {}
for code, patterns in keywords.items():
    for pattern in patterns:
        match = re.search(pattern + r'.*?(\d{1,3}(?:\.\d{3})+)', text)
        if match:
            num_str = match.group(1).replace('.', '')
            financials[code] = int(num_str)
            break

mst_match = re.search(r'mã số thuế.*?(0\d{9})', text)
if mst_match:
    financials['MST'] = mst_match.group(1)

print(financials.get("MST"))
print(financials.get("IS_REVENUE"))
