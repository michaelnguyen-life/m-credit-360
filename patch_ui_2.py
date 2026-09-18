import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update EB buttons
old_eb_btns = '''<button onclick="loadSampleEB('alpha')" class="px-3 py-1.5 rounded-lg bg-[#F8F9FA] hover:bg-slate-100 text-[#344054] border border-[#E6EAF0] flex items-center gap-1.5 transition text-[11px]">
                <i data-lucide="building-2" class="w-3.5 h-3.5 text-[#667085]"></i> Mock: Tp oAn Alpha (FMCG)
              </button>
              <button onclick="loadSampleEB('beta')" class="px-3 py-1.5 rounded-lg bg-[#F8F9FA] hover:bg-slate-100 text-[#344054] border border-[#E6EAF0] flex items-center gap-1.5 transition text-[11px]">
                <i data-lucide="factory" class="w-3.5 h-3.5 text-[#667085]"></i> Mock: CA"ng ngh Beta (Sn xut)
              </button>'''

new_eb_btns = '''<button onclick="loadSampleEB('eb_good_1')" class="px-3 py-1.5 rounded-lg bg-[#ECFDF3] hover:bg-[#D1FADF] text-[#027A48] border border-[#A6F4C5] flex items-center gap-1.5 transition text-[11px]">
                <i data-lucide="check-circle" class="w-3.5 h-3.5 text-[#12B76A]"></i> Tốt 1: Khang Thịnh
              </button>
              <button onclick="loadSampleEB('eb_good_2')" class="px-3 py-1.5 rounded-lg bg-[#ECFDF3] hover:bg-[#D1FADF] text-[#027A48] border border-[#A6F4C5] flex items-center gap-1.5 transition text-[11px]">
                <i data-lucide="check-circle" class="w-3.5 h-3.5 text-[#12B76A]"></i> Tốt 2: Vinamilk
              </button>
              <button onclick="loadSampleEB('eb_bad_1')" class="px-3 py-1.5 rounded-lg bg-[#FEF3F2] hover:bg-[#FEE4E2] text-[#B42318] border border-[#FECDCA] flex items-center gap-1.5 transition text-[11px]">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-[#F04438]"></i> Xấu 1: FLC
              </button>
              <button onclick="loadSampleEB('eb_bad_2')" class="px-3 py-1.5 rounded-lg bg-[#FEF3F2] hover:bg-[#FEE4E2] text-[#B42318] border border-[#FECDCA] flex items-center gap-1.5 transition text-[11px]">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-[#F04438]"></i> Xấu 2: Tân Hoàng Minh
              </button>'''
# Using regex to replace the buttons robustly
content = re.sub(r'<button onclick="loadSampleEB\(\'alpha\'\).*?</button>\s*<button onclick="loadSampleEB\(\'beta\'\).*?</button>', new_eb_btns, content, flags=re.DOTALL)

# 2. Update RB buttons
old_rb_btns = '''<button onclick="loadSampleRB('tiktok')" class="px-3 py-1.5 rounded-lg bg-[#F8F9FA] hover:bg-slate-100 text-[#344054] border border-[#D0D5DD] flex items-center gap-1.5 transition">
              <i data-lucide="shopping-bag" class="w-4 h-4 text-[#FF5A00]"></i> Load mu TikTok Shop
            </button>'''

new_rb_btns = '''<button onclick="loadSampleRB('rb_good_1')" class="px-3 py-1.5 rounded-lg bg-[#ECFDF3] hover:bg-[#D1FADF] text-[#027A48] border border-[#A6F4C5] flex items-center gap-1.5 transition text-[11px]">
              <i data-lucide="check-circle" class="w-3.5 h-3.5 text-[#12B76A]"></i> Tốt 1: TikTok Shop
            </button>
            <button onclick="loadSampleRB('rb_good_2')" class="px-3 py-1.5 rounded-lg bg-[#ECFDF3] hover:bg-[#D1FADF] text-[#027A48] border border-[#A6F4C5] flex items-center gap-1.5 transition text-[11px]">
              <i data-lucide="check-circle" class="w-3.5 h-3.5 text-[#12B76A]"></i> Tốt 2: Shopee Mall
            </button>
            <button onclick="loadSampleRB('rb_bad_1')" class="px-3 py-1.5 rounded-lg bg-[#FEF3F2] hover:bg-[#FEE4E2] text-[#B42318] border border-[#FECDCA] flex items-center gap-1.5 transition text-[11px]">
              <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-[#F04438]"></i> Xấu 1: Livestream Ảo
            </button>
            <button onclick="loadSampleRB('rb_bad_2')" class="px-3 py-1.5 rounded-lg bg-[#FEF3F2] hover:bg-[#FEE4E2] text-[#B42318] border border-[#FECDCA] flex items-center gap-1.5 transition text-[11px]">
              <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-[#F04438]"></i> Xấu 2: D.Thu Cắm Đầu
            </button>'''
content = re.sub(r'<button onclick="loadSampleRB\(\'tiktok\'\).*?</button>', new_rb_btns, content, flags=re.DOTALL)

# 3. Update extraction modal mapping (dataMap) in JS
new_dataMap = '''const dataMap = {
        'eb_good_1': {
            name: 'CÔNG TY TNHH XD - TTNT KHANG THỊNH', tax: '0305956840', rev: '20.278.122.298', revShort: '20,27 tỷ', 
            ebit: '34.825.664', assets: '25.818.411.666', liab: '20.534.512.914'
        },
        'eb_good_2': {
            name: 'CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)', tax: '0300588569', rev: '60.000.000.000.000', revShort: '60.000 tỷ', 
            ebit: '12.000.000.000.000', assets: '35.000.000.000.000', liab: '15.000.000.000.000'
        },
        'eb_bad_1': {
            name: 'CÔNG TY CỔ PHẦN TẬP ĐOÀN FLC', tax: '0102683813', rev: '427.000.000.000', revShort: '427 tỷ', 
            ebit: '-785.000.000.000', assets: '15.000.000.000.000', liab: '18.000.000.000.000'
        },
        'eb_bad_2': {
            name: 'TẬP ĐOÀN TÂN HOÀNG MINH', tax: '0101010101', rev: '1.500.000.000.000', revShort: '1.500 tỷ', 
            ebit: '-1.200.000.000.000', assets: '25.000.000.000.000', liab: '45.000.000.000.000'
        },
        'alpha': {
            name: 'CÔNG TY CỔ PHẦN TẬP ĐOÀN ALPHA', tax: '0311807068', rev: '318.000.000.000', revShort: '318,00 tỷ', 
            ebit: '18.500.000.000', assets: '120.000.000.000', liab: '145.000.000.000'
        }
      };'''
content = re.sub(r'const dataMap = \{.*?^\s*\}\;', new_dataMap, content, flags=re.DOTALL|re.MULTILINE)

# 4. Update file detection logic
old_detect = '''let detectedType = 'alpha';
            const lowerName = currentUploadedFileName.toLowerCase();
            if (lowerName.includes('beta')) detectedType = 'beta';
            else if (lowerName.includes('khang') || lowerName.includes('thinh')) detectedType = 'khangthinh';
            else if (lowerName.includes('flc')) detectedType = 'flc';'''

new_detect = '''let detectedType = 'alpha';
            const lowerName = currentUploadedFileName.toLowerCase();
            if (lowerName.includes('khang') || lowerName.includes('thinh')) detectedType = 'eb_good_1';
            else if (lowerName.includes('vinamilk') || lowerName.includes('vnm')) detectedType = 'eb_good_2';
            else if (lowerName.includes('flc')) detectedType = 'eb_bad_1';
            else if (lowerName.includes('tanhoangminh') || lowerName.includes('thm')) detectedType = 'eb_bad_2';'''

content = content.replace(old_detect, new_detect)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
