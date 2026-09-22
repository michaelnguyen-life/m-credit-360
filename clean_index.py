import os
import re

file_path = "templates/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove navigation links except "Thẩm định AI"
content = re.sub(r'<a href="#overview".*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#customers".*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#reports".*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#documents".*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#cross-sell".*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#tools".*?</a>', '', content, flags=re.DOTALL)
content = re.sub(r'<a href="#settings".*?</a>', '', content, flags=re.DOTALL)

# 2. Remove Right Header Actions (Search bar & Notification Bell)
# Replace the block from Search bar to Notification Bell
content = re.sub(r'<!-- Search bar -->.*?<!-- User Profile -->', '<!-- User Profile -->', content, flags=re.DOTALL)

# 3. Remove Box 1 dummy files. Keep the list container empty.
content = re.sub(r'<div id="file-ingested-list".*?</div>\s*</div>\s*<button onclick="openUploadDrawer\(\)"', '<div id="file-ingested-list" class="space-y-1.5 text-xs"></div>\n\n            <button onclick="openUploadDrawer()"', content, flags=re.DOTALL)

# 4. Remove Copilot Action Buttons from Box 2
content = re.sub(r'<!-- Copilot Action Buttons -->.*?</div>\s*</div>\s*</div>\s*</div>\s*<!-- ==================== TAB 2', '</div>\n\n        </div>\n      </div>\n\n      <!-- ==================== TAB 2', content, flags=re.DOTALL)

# 5. Remove FLOATING AI CHAT COPILOT DRAWER & FLOATING CHAT BUTTON TRIGGER
content = re.sub(r'<!-- ==================== FLOATING AI CHAT COPILOT DRAWER ==================== -->.*?<!-- ==================== JAVASCRIPT LOGIC ==================== -->', '<!-- ==================== JAVASCRIPT LOGIC ==================== -->', content, flags=re.DOTALL)

# 6. Remove Javascript functions for chat
content = re.sub(r'function toggleChatDrawer\(\) \{.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'function triggerAICopilot\(promptText\) \{.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'// 12\. Chat Copilot Message Sending.*?window\.addEventListener', 'window.addEventListener', content, flags=re.DOTALL)

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Cleanup complete!")
