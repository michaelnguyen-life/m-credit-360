import os
import re

file_path = "templates/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Change Column 1 span from 4 to 5
content = re.sub(r'<!-- COLUMN 1: COMPANY DATA \(approx 31%\) -->\s*<div class="xl:col-span-4', 
                 '<!-- COLUMN 1: COMPANY DATA -->\n        <div class="xl:col-span-5', content)

# Change Column 2 span from 5 to 7
content = re.sub(r'<!-- COLUMN 2: ANALYSIS & UNDERWRITING \(approx 44%\) -->\s*<div class="xl:col-span-5', 
                 '<!-- COLUMN 2: ANALYSIS & UNDERWRITING -->\n        <div class="xl:col-span-7', content)

# Delete Column 3 completely
content = re.sub(r'<!-- COLUMN 3: RIGHT PANEL.*?</div>\s*</div>\s*</div>\s*<!-- ==================== TAB 2',
                 '</div>\n      </div>\n\n      <!-- ==================== TAB 2', content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Layout updated.")
