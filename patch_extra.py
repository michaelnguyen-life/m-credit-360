import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "Thêm chỉ tiêu khác" button with one that toggles a panel
button_html = r'<button class="w-full mt-3 py-2 border border-dashed border-\[\#CBD5E1\] text-\[\#64748B\].*?Thêm chỉ tiêu khác</button>'
new_button = """<button type="button" onclick="document.getElementById('extra-criteria-panel').classList.toggle('hidden')" class="w-full mt-3 py-2 border border-dashed border-[#CBD5E1] text-[#64748B] text-xs font-semibold rounded-lg hover:bg-slate-50 transition flex items-center justify-center gap-1.5"><i data-lucide="plus" class="w-3.5 h-3.5"></i>Thêm chỉ tiêu khác</button>
                
                <div id="extra-criteria-panel" class="hidden mt-2 p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-2">
                    <p class="font-bold text-slate-700">Yêu cầu phân tích nâng cao từ File gốc:</p>
                    <label class="flex items-center gap-2"><input type="checkbox" checked /> Chỉ tiêu cân đối tài khoản (Thực-Ảo)</label>
                    <label class="flex items-center gap-2"><input type="checkbox" checked /> Top 5 Khách hàng đầu vào lớn nhất</label>
                    <label class="flex items-center gap-2"><input type="checkbox" checked /> Top 5 Khách hàng đầu ra lớn nhất</label>
                    <button type="button" class="mt-2 w-full py-1.5 bg-[#0B1739] text-white rounded font-medium" onclick="showToast('Đã thêm các chỉ tiêu lọc thành công!', 'info'); document.getElementById('extra-criteria-panel').classList.add('hidden')">Áp dụng Lọc</button>
                </div>"""

content = re.sub(button_html, new_button, content, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated extra criteria")
