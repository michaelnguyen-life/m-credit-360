import docx, io

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
t = doc.tables[0]

rows_to_check = [1, 3, 5, 9, 12, 21, 22, 70, 72, 73, 84, 85, 95, 96]

with io.open('mb01a_row_cells.txt', 'w', encoding='utf-8') as out:
    for r in rows_to_check:
        out.write(f'=== ROW {r} ===\n')
        for c_idx, c in enumerate(t.rows[r].cells):
            # Print unique non-empty
            out.write(f'  Col {c_idx:2d}: {repr(c.text.strip())}\n')

print('Detailed row cells written')
