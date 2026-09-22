import io
import re

with io.open('server.py', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Replace everything from `mst = "0101234567"` up to `# Check if text is completely empty`
start = text.find('mst = "0101234567"')
end = text.find('# Check if text is completely empty (Scanned PDF)')

new_logic = """mst = "0101234567"
    company_name = file.filename.split('.')[0].replace('_', ' ').upper()
    if not company_name.startswith("CÔNG TY") and not company_name.startswith("CTY"):
        company_name = "CTY " + company_name
        
    # Extract REAL Company Name from text
    # We will search for 'công ty' and take up to 80 chars
    company_match = re.search(r'(công ty\s+(?:tnhh|cp|cổ phần|trách nhiệm|tập đoàn)[^\n]{5,80})', text.lower())
    if company_match:
        company_name = company_match.group(1).upper().strip()
    else:
        # Just find any line starting with Công ty
        company_match = re.search(r'(công ty[^\n]{5,80})', text.lower())
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
            
    """

text = text[:start] + new_logic + text[end:]

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)
