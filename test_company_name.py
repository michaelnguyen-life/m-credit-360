import re
from pypdf import PdfReader

try:
    reader = PdfReader('data_test/BCTC 2025 ĐK.pdf')
    text = reader.pages[0].extract_text() or ""
    
    # Let's find company name
    match = re.search(r'(?:tên người nộp thuế|đơn vị|công ty)[:\s]*(công ty[^\n]+)', text.lower())
    if match:
        print(match.group(1))
    else:
        # Just find the first occurrence of "công ty"
        match = re.search(r'(công ty[^\n]+)', text.lower())
        if match:
            print(match.group(1))
except Exception as e:
    print(e)
