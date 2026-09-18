with open('live_html.txt', 'r', encoding='utf-8') as f:
    html = f.read()

import re
scripts = re.findall(r'<script[^>]*>([\s\S]*?)<\/script>', html, re.IGNORECASE)
print(f"Found {len(scripts)} script tags")

for i, s in enumerate(scripts):
    print(f"\n--- Script {i} (Length: {len(s)}) ---")
    print(s[:200].strip())

if "Tỷ" in html:
    print("\nContains 'Tỷ': YES")
if "function saveDraftNotification" in html:
    print("Contains 'saveDraftNotification': YES")
if "setupSidebar" in html:
    print("Contains 'setupSidebar': YES")
