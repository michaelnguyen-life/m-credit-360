import docx, io

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
t = doc.tables[0]

with io.open('mb01a_fill_check.txt', 'w', encoding='utf-8') as out:
    for r in [1, 3, 5, 9, 12, 13, 21, 22, 68, 70, 72, 73, 85]:
        out.write(f'--- ROW {r} ---\n')
        for c in range(len(t.rows[r].cells)):
            txt = t.rows[r].cells[c].text.strip()
            if txt:
                out.write(f'  Col {c}: {repr(txt[:40])}\n')

print('Checked fill locations')
