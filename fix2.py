with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First revert everything back
content = content.replace(': False,', ': false,')
content = content.replace(': True,', ': true,')
content = content.replace(': True}', ': true}')
content = content.replace(': False}', ': false}')

# Now only fix my specific Python dicts which start at EB_GOOD_1 (line ~688) up to the end of RB_BAD_2
# Actually, I can just change my python dicts to use strings "False" / "True", or I can just fix them manually.
# Let's write a regex to find python dict blocks and fix them, or just let python handle the strings.

# Wait, the only variables that need 'False' / 'True' are in my added text.
# Let's just fix the documents blocks in my added text:
fix1 = '''  "documents": {
    "identity": true,
    "income_proof": true,
    "cic": true,
    "business_registration": true,
    "platform_evidence": true
  }'''
res1 = '''  "documents": {
    "identity": True,
    "income_proof": True,
    "cic": True,
    "business_registration": True,
    "platform_evidence": True
  }'''
content = content.replace(fix1, res1)

fix2 = '''  "documents": {
    "identity": true,
    "income_proof": false,
    "cic": true,
    "business_registration": false,
    "platform_evidence": false
  }'''
res2 = '''  "documents": {
    "identity": True,
    "income_proof": False,
    "cic": True,
    "business_registration": False,
    "platform_evidence": False
  }'''
content = content.replace(fix2, res2)

fix3 = '''  "documents": {
    "identity": true,
    "income_proof": true,
    "cic": true,
    "business_registration": false,
    "platform_evidence": true
  }'''
res3 = '''  "documents": {
    "identity": True,
    "income_proof": True,
    "cic": True,
    "business_registration": False,
    "platform_evidence": True
  }'''
content = content.replace(fix3, res3)

# And the loan secured field:
content = content.replace('''"secured": false,
    "purpose": "Nhập hàng mùa Tết"''', '''"secured": False,
    "purpose": "Nhập hàng mùa Tết"''')
content = content.replace('''"secured": false,
    "purpose": "Gồng lỗ chi phí quảng cáo"''', '''"secured": False,
    "purpose": "Gồng lỗ chi phí quảng cáo"''')
content = content.replace('''"secured": false,
    "purpose": "Vay đảo nợ"''', '''"secured": False,
    "purpose": "Vay đảo nợ"''')


with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
