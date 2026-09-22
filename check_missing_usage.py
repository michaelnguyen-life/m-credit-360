import io

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

missing_keys = ['btn-save-eb', 'eb-fcf', 'eb-gp', 'eb-icf', 'eb-np', 'eb-ocf', 'eb-short-debt', 'eb-std', 'eb-tl']

with io.open('missing_id_locations.txt', 'w', encoding='utf-8') as out:
    for k in missing_keys:
        out.write(f"=== KEY: {k} ===\n")
        idx = html.find(f"'{k}'")
        if idx == -1:
            idx = html.find(f'"{k}"')
        while idx != -1:
            start = max(0, idx - 60)
            end = min(len(html), idx + 100)
            out.write(f"  Pos {idx}: {html[start:end].replace(chr(10), ' ')}\n")
            idx = html.find(f"'{k}'", idx + 1)
            if idx == -1:
                idx = html.find(f'"{k}"', idx + 1)

print("Wrote missing_id_locations.txt")
