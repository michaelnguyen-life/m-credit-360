import docx, io

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
t = doc.tables[0]

rows_to_check = [0, 1, 3, 4, 5, 9, 12, 13, 21, 22, 68, 70, 72, 73, 84, 85, 95, 96]

with io.open('mb01a_unique_cells.txt', 'w', encoding='utf-8') as out:
    for r in rows_to_check:
        out.write(f'=== ROW {r} ===\n')
        seen_cells = set()
        for c_idx, c in enumerate(t.rows[r].cells):
            cell_id = id(c._tc)
            if cell_id not in seen_cells:
                seen_cells.add(cell_id)
                out.write(f'  Col {c_idx:2d}: {repr(c.text.strip())}\n')

print('Unique row cells written')
