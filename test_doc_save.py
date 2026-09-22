import docx

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
t = doc.tables[0]

# Row 3: Họ tên
print("Before R3:", repr(t.rows[3].cells[0].text))
t.rows[3].cells[0].text = "Họ tên: PHẠM THANH BÌNH"
print("After R3:", repr(t.rows[3].cells[0].text))

# Row 5: CCCD
print("Before R5 Col 11:", repr(t.rows[5].cells[11].text))
t.rows[5].cells[11].text = "079090123456"
print("After R5 Col 11:", repr(t.rows[5].cells[11].text))

# Row 1: Hạn mức đề nghị
t.rows[1].cells[0].text = "Hạn mức tín dụng đề nghị cấp: 450.000.000 VND (Bằng chữ: Bốn trăm năm mươi triệu đồng)"

doc.save("test_filled_mb01a.docx")
print("Saved test_filled_mb01a.docx successfully!")
