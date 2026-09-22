import json

with open('extracted_pdfs.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('_bctc_text.txt', 'w', encoding='utf-8') as out:
    out.write('=== BCTC 2025 ===\n')
    out.write(d['BCTC_2025']['text'])
    out.write('\n\n=== GCN ===\n')
    out.write(d['GCN']['text'])
    out.write('\n\n=== CCCD ===\n')
    out.write(d['CCCD']['text'])
    out.write('\n\n=== SAO KE (first 3) ===\n')
    for sp in d['sao_ke_list'][:3]:
        out.write('\n--- ' + sp['file'] + ' ---\n')
        out.write(sp['text'])

print('Done - _bctc_text.txt')
