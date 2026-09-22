import io
import re
with io.open('templates/temp_backup.html', 'r', encoding='utf-8') as f:
    html = f.read()

eb_start = html.find('id="section-eb"')
part = html[eb_start:eb_start+500]
print(re.findall(r'xl:col-span-\d+', part))
