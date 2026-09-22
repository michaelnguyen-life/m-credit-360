import io, re

with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# All element IDs referenced in JS
ids_in_js = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', html)
unique_ids = sorted(list(set(ids_in_js)))
print(f"Total unique IDs referenced in JS: {len(unique_ids)}")

with io.open('id_audit.txt', 'w', encoding='utf-8') as out:
    missing_ids = []
    for el_id in unique_ids:
        # Check if id="el_id" exists in HTML
        pattern = f'id="{el_id}"'
        pattern_single = f"id='{el_id}'"
        exists = (pattern in html) or (pattern_single in html)
        if not exists:
            missing_ids.append(el_id)
            out.write(f"MISSING: {el_id}\n")
        else:
            out.write(f"OK: {el_id}\n")

print(f"Total missing IDs: {len(missing_ids)}")
for m in missing_ids:
    print("  -> MISSING:", m)
