import io
import re

from pypdf import PdfReader
reader = PdfReader('data_test/BCTC 2025 ĐK.pdf')
text = reader.pages[2].extract_text() or ""
for ch in range(1, 32):
    if ch != 10:
        text = text.replace(chr(ch), ' ')

lines = text.lower().split('\n')
for line in lines:
    if "doanh thu thuần" in line:
        print(repr(line))
        numbers = re.findall(r'-?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?', line)
        print(numbers)
