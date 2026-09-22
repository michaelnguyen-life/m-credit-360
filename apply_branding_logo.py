import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title
content = content.replace('<title>M-Credit 360 AI | SME AI Banking Workspace</title>', '<title>M-Insight 360 AI | SME AI Banking Workspace</title>')

# 2. Update Sidebar Branding
content = content.replace('<span class="font-bold text-[11px] text-[#0B1739] block">M-CREDIT 360</span>', '<span class="font-bold text-[11px] text-[#0B1739] block">M-Insight 360</span>')

# 3. Update Top Header Branding
content = content.replace('<span class="text-base font-black tracking-tight text-[#0B1739]">M-CREDIT <span class="text-[#FF5A00]">360</span></span>', '<span class="text-base font-black tracking-tight text-[#0B1739]">M-Insight <span class="text-[#FF5A00]">360</span></span>')

# 4. Update Box 2 AI Insight Header
content = content.replace('<span>M-CREDIT AI Insight</span>', '<span>M-Insight AI</span>')
content = content.replace('<!-- Box 2: M-CREDIT AI Insight -->', '<!-- Box 2: M-Insight AI -->')

# 5. Update Drawer Processing text
content = content.replace('<span>M-CREDIT AI đang xử lý hồ sơ...</span>', '<span>M-Insight AI đang xử lý hồ sơ...</span>')

# 6. Clear Alpha Group in upload-file-rows
old_alpha_block = '''          <div id="upload-file-rows" class="space-y-1.5 max-h-48 overflow-y-auto">
            <div class="p-2.5 rounded-lg bg-slate-50 border border-[#E6EAF0] flex items-center justify-between text-xs">
              <div class="flex items-center gap-2 truncate">
                <span class="w-5 h-5 rounded bg-red-100 text-red-600 font-bold text-[9px] flex items-center justify-center font-mono">PDF</span>
                <span class="font-medium text-[#0B1739] truncate">BCTC_2025_Alpha_Group.pdf</span>
              </div>
              <span class="text-[10px] text-[#00A86B] font-medium flex items-center gap-1">
                <i data-lucide="check" class="w-3 h-3"></i> Đã bóc tách
              </span>
            </div>
          </div>'''

new_alpha_block = '''          <div id="upload-file-rows" class="space-y-1.5 max-h-48 overflow-y-auto">
            <!-- Files dynamically added when selected -->
          </div>'''

if old_alpha_block in content:
    content = content.replace(old_alpha_block, new_alpha_block)
    print('Cleaned Alpha Group from upload-file-rows')
else:
    print('Alpha Group block not matched directly, checking...')

# 7. Update Chat Drawer Header Icon & Floating Chat Trigger Button with Logo
old_drawer_header_icon = '''        <div class="w-8 h-8 rounded-lg bg-[#FF5A00] flex items-center justify-center text-white">
          <i data-lucide="bot" class="w-5 h-5"></i>
        </div>'''

new_drawer_header_icon = '''        <div class="w-8 h-8 rounded-lg overflow-hidden flex items-center justify-center bg-white border border-[#E6EAF0] shadow-sm">
          <img src="/static/img/m_insight_logo.png" alt="M-Insight Logo" class="w-full h-full object-cover" />
        </div>'''

content = content.replace(old_drawer_header_icon, new_drawer_header_icon)

# Floating button
old_floating_btn = '''  <!-- FLOATING CHAT BUTTON TRIGGER -->
  <button onclick="toggleChatDrawer()" class="fixed bottom-14 right-6 z-30 p-3 rounded-2xl bg-[#FF5A00] hover:bg-[#EA4E00] text-white shadow-lg shadow-orange-500/25 hover:scale-105 transition">
    <i data-lucide="message-circle" class="w-5 h-5"></i>
  </button>'''

new_floating_btn = '''  <!-- FLOATING CHAT BUTTON TRIGGER WITH LOGO -->
  <button onclick="toggleChatDrawer()" title="M-Insight 360 Copilot" class="fixed bottom-14 right-6 z-30 w-12 h-12 rounded-2xl bg-white hover:bg-orange-50 p-1 border-2 border-[#FF5A00] shadow-xl shadow-orange-500/25 hover:scale-105 transition flex items-center justify-center overflow-hidden group">
    <img src="/static/img/m_insight_logo.png" alt="M-Insight Logo" class="w-full h-full object-contain rounded-xl group-hover:scale-110 transition duration-200" />
  </button>'''

content = content.replace(old_floating_btn, new_floating_btn)

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Update successfully applied!')
