import os
import re

file_path = "templates/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove Box 2: M-CREDIT AI Insight
# It starts with <!-- Box 2: M-CREDIT AI Insight --> and goes until the end of the div (which is followed by </div> </div> <!-- ==================== TAB 2)
content = re.sub(r'<!-- Box 2: M-CREDIT AI Insight -->.*?</div>\s*</div>\s*</div>\s*<!-- ==================== TAB 2', '</div>\n\n        </div>\n      </div>\n\n      <!-- ==================== TAB 2', content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Box 2 removed")
