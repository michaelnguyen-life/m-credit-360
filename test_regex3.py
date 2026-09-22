import re

text = "doanh thu thuần về bán hàng và cung cấp dịch vụ (10= 01-02)1020.278.122.29823.157.909.231"

# find first number after keyword
match = re.search(r'doanh thu thuần.*?(\d{1,3}(?:\.\d{3})+)', text)
if match:
    print(match.group(1))
