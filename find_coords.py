import docx, io

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
table = doc.tables[0]

keywords = [
    'Họ tên:', 'Số CCCD/Hộ chiếu:', 'Điện thoại di động:', 'Địa chỉ thường trú:',
    'Tên cơ sở kinh doanh*:', 'Ngành nghề kinh doanh*:', 'Hạn mức tín dụng đề nghị cấp:',
    'Thu nhập từ kinh doanh', 'Thu nhập từ lương', 'TỔNG THU NHẬP (A)', 'TỔNG CHI PHÍ (B)',
    'Thu nhập tích lũy hàng tháng*', 'Số tiền đề nghị vay:', 'Thời hạn:'
]

with io.open('mb01a_matches.txt', 'w', encoding='utf-8') as out:
    for kw in keywords:
        found = False
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if kw.lower() in cell.text.lower():
                    out.write(f'Match: "{kw}" at Row {r_idx}, Col {c_idx} -> cell text: {repr(cell.text[:60])}\n')
                    found = True
                    break
            if found:
                break

print('Coordinates written to mb01a_matches.txt')
