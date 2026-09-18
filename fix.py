with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Regex to remove the entire DYNAMIC CROSS-SELL MOCK block
pattern = r"\s*// DYNAMIC CROSS-SELL MOCK.*?\} catch\(e\) \{ console\.error\(\"Cross-sell update failed:\", e\); \}\n"
content = re.sub(pattern, "", content, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
