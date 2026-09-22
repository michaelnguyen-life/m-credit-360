import docx

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
t = doc.tables[0]

t.rows[3].cells[0].text = "Họ tên: PHẠM THANH BÌNH"
t.rows[5].cells[11].text = "079090123456"
t.rows[1].cells[0].text = "Hạn mức tín dụng đề nghị cấp: 450.000.000 VND (Bằng chữ: Bốn trăm năm mươi triệu đồng)"

doc.save("test_filled_mb01a.docx")
import os
print("Saved:", os.path.exists("test_filled_mb01a.docx"), "Size:", os.path.getsize("test_filled_mb01a.docx"))
