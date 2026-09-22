import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update upload drawer text
html = html.replace('Khởi động AI Engine (MaaS)...', 'Khởi động GreenNode MaaS LLM (Qwen 3.6 Flash)...')
html = html.replace('AI Đọc hiểu & Bóc tách BCTC...', 'AI Đọc hiểu & Bóc tách BCTC (Zero-Regex)...')
html = html.replace('Quét rủi ro pháp lý & OSINT 360°...', 'Quét rủi ro pháp lý & OSINT 360° đa tầng...')

with io.open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
