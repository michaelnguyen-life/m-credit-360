import docx, io

doc_path = r'C:\Users\finan\OneDrive\Documents\02. DU AN AI & CONG NGHE\THUONG THUONG AI\32_HATTRICK\MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx'
doc = docx.Document(doc_path)
t = doc.tables[0]

with io.open('mb01a_all_labels.txt', 'w', encoding='utf-8') as out:
    for r_idx, row in enumerate(t.rows):
        seen = set()
        labels = []
        for c_idx, cell in enumerate(row.cells):
            cid = id(cell._tc)
            if cid not in seen:
                seen.add(cid)
                txt = cell.text.replace('\n', ' ').strip()
                if txt:
                    labels.append(f'[{c_idx}]: {txt[:40]}')
        if labels:
            out.write(f'R{r_idx:2d}: ' + ' | '.join(labels) + '\n')

print('All row labels written')
