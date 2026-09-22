import io
import re

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update Company Name extraction logic
old_mst_logic = '''    # Try to extract MST and Company Name if possible
    mst = "0101234567"
    company_name = "CTY " + file.filename.split('.')[0].replace('_', ' ').upper()
    mst_match = re.search(r'mã số thuế.*?(0\d{9})', text.lower())
    if mst_match:
        mst = mst_match.group(1)
    else:
        mst_match = re.search(r'(?:mã số doanh nghiệp|mst)[:\s-]*(\d{10,14})', text.lower())
        if mst_match:
            mst = mst_match.group(1)'''

new_mst_logic = '''    # Try to extract MST and Company Name if possible
    mst = "0101234567"
    company_name = "CTY " + file.filename.split('.')[0].replace('_', ' ').upper()
    
    # 1. Extract REAL Company Name from text
    # Look for "tên người nộp thuế: công ty..." or just "công ty..."
    company_match = re.search(r'(?:tên người nộp thuế|đơn vị)[:\s]*(công ty[^\n]+)', text.lower())
    if company_match:
        company_name = company_match.group(1).upper().strip()
    else:
        company_match = re.search(r'(công ty[^\n]+)', text.lower())
        if company_match:
            company_name = company_match.group(1).upper().strip()
            
    # Clean up company name
    company_name = re.sub(r'[^A-ZĂÂĐÊÔƠƯÀẢÃÁẠẰẲẴẮẶẦẨẪẤẬÈẺẼÉẸỀỂỄẾỆÌỈĨÍỊÒỎÕÓỌỒỔỖỐỘỜỞỠỚỢÙỦŨÚỤỪỬỮỨỰỲỶỸÝỴ0-9 -]', '', company_name)
    if len(company_name) > 60:
        company_name = company_name[:60] + "..."
            
    mst_match = re.search(r'mã số thuế.*?(0\d{9})', text.lower())
    if mst_match:
        mst = mst_match.group(1)
    else:
        mst_match = re.search(r'(?:mã số doanh nghiệp|mst)[:\s-]*(\d{10,14})', text.lower())
        if mst_match:
            mst = mst_match.group(1)
            
    # Check if text is completely empty (Scanned PDF)
    if len(text.strip()) < 50:
        company_name = "KHÔNG ĐỌC ĐƯỢC CHỮ (FILE SCAN/ẢNH)"
        mst = "KHÔNG RÕ"
'''

code = code.replace(old_mst_logic, new_mst_logic)

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
