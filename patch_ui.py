import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update JS dataMap
new_dataMap = '''const dataMap = {
        'alpha': {
            name: 'CÔNG TY CỔ PHẦN TẬP ĐOÀN ALPHA', tax: '0311807068', rev: '318.000.000.000', revShort: '318,00 tỷ', 
            ebit: '18.500.000.000', assets: '120.000.000.000', liab: '145.000.000.000'
        },
        'beta': {
            name: 'CÔNG TY CỔ PHẦN CÔNG NGHỆ BETA', tax: '0319888999', rev: '280.000.000.000', revShort: '280,00 tỷ', 
            ebit: '32.000.000.000', assets: '185.000.000.000', liab: '92.000.000.000'
        },
        'khangthinh': {
            name: 'CÔNG TY TNHH XD - TTNT KHANG THỊNH', tax: '0305956840', rev: '20.278.122.298', revShort: '20,27 tỷ', 
            ebit: '34.825.664', assets: '25.818.411.666', liab: '20.534.512.914'
        },
        'flc': {
            name: 'CÔNG TY CỔ PHẦN TẬP ĐOÀN FLC', tax: '0102683813', rev: '427.000.000.000', revShort: '427,00 tỷ', 
            ebit: '-785.000.000.000', assets: '15.000.000.000.000', liab: '18.000.000.000.000'
        }
      };'''

content = re.sub(r'const dataMap = \{.*?^\s*\}\;', new_dataMap, content, flags=re.DOTALL|re.MULTILINE)

# Update filename detection
old_detect = '''let detectedType = 'alpha';
            const lowerName = currentUploadedFileName.toLowerCase();
            if (lowerName.includes('beta')) detectedType = 'beta';
            else if (lowerName.includes('khang') || lowerName.includes('thinh')) detectedType = 'khangthinh';'''

new_detect = '''let detectedType = 'alpha';
            const lowerName = currentUploadedFileName.toLowerCase();
            if (lowerName.includes('beta')) detectedType = 'beta';
            else if (lowerName.includes('khang') || lowerName.includes('thinh')) detectedType = 'khangthinh';
            else if (lowerName.includes('flc')) detectedType = 'flc';'''

content = content.replace(old_detect, new_detect)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
