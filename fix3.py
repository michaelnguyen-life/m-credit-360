with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We know the python dicts start after EB_BAD_2 and end before get_sample_eb
# Let's just find RB_GOOD_2, RB_BAD_1, RB_BAD_2 and replace true/false with True/False inside them.

def replacer(match):
    text = match.group(0)
    text = re.sub(r':\s*true', ': True', text)
    text = re.sub(r':\s*false', ': False', text)
    return text

content = re.sub(r'RB_GOOD_2 = \{.*?\}  # placeholder', replacer, content, flags=re.DOTALL)
content = re.sub(r'RB_GOOD_2 = \{.*?^\}', replacer, content, flags=re.DOTALL|re.MULTILINE)
content = re.sub(r'RB_BAD_1 = \{.*?^\}', replacer, content, flags=re.DOTALL|re.MULTILINE)
content = re.sub(r'RB_BAD_2 = \{.*?^\}', replacer, content, flags=re.DOTALL|re.MULTILINE)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
