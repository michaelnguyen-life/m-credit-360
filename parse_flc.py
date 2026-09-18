import pymupdf
import os

pdf_path = r"C:\Users\finan\OneDrive\Desktop\FLC_22Q3_BCTC_M.pdf"

if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
else:
    try:
        doc = pymupdf.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        with open('flc.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Success, lines:", len(text.split('\n')))
    except Exception as e:
        print("Error:", e)
