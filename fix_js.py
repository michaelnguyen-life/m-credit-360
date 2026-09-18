with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(
    r'statusSpan\.innerHTML = <span class="w-1\.5 h-1\.5 rounded-full bg-\[#00A86B\]"></span><span>.*?</span>;',
    'statusSpan.innerHTML = \'<span class="w-1.5 h-1.5 rounded-full bg-[#00A86B]"></span><span>Đã lưu nháp \' + timeStr + \'</span>\';',
    content
)
content = re.sub(
    r"showToast\(.*?Đã lưu nháp lúc.*?, 'info'\);",
    "showToast('Đã lưu nháp lúc ' + timeStr, 'info');",
    content
)
content = re.sub(
    r'a\.download = To_Trinh_MB02a_\.docx;',
    "a.download = 'To_Trinh_MB02a_' + taxId + '.docx';",
    content
)
content = re.sub(
    r'btn\.innerHTML = <i data-lucide="loader-2".*?</span>;',
    'btn.innerHTML = \'<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>Đang xử lý...</span>\';',
    content
)
content = re.sub(
    r'throw new Error\(HTTP Error .*?\);',
    "throw new Error('HTTP Error ' + res.status);",
    content
)
content = re.sub(
    r"showToast\(.*?Đang tìm kiếm: .*?, 'info'\);",
    "showToast('Đang tìm kiếm: ' + val, 'info');",
    content
)
content = re.sub(
    r"titleSec\.textContent = 'MÔ ĐUN: ' \+ link\.textContent\.trim\(\)\.toUpperCase\(\);",
    "titleSec.textContent = 'MÔ ĐUN: ' + link.textContent.trim().toUpperCase();",
    content
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
