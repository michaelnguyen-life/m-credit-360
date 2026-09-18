# -*- coding: utf-8 -*-
import codecs

content = codecs.open('templates/index.html', 'r', 'utf-8').read()
content = content.replace("a.download = 'To_Trinh_MB02a_' + taxId + '.docx';", "a.download = 'To_Trinh_MB02a_' + payload.company.tax_id + '.docx';")
codecs.open('templates/index.html', 'w', 'utf-8').write(content)
