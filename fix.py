with open('agents/eb_credit_agent.py', 'r', encoding='utf-8') as f:
    js = f.read()

import re
js = re.sub(r'x\n"([^)])', r'x\\n"\1', js)
js = re.sub(r'cfo\)\}\n"([^)])', r'cfo\)\}\\n"\1', js)
js = re.sub(r"Không'\n", r"Không'\\n", js)
js = js.replace('x\n            f"DSCR', 'x\\n"            f"DSCR')
js = js.replace('x\n            f"Net Margin', 'x\\n"            f"Net Margin')
js = js.replace('roe)}\n            f"D/E', 'roe)}\\n"            f"D/E')
js = js.replace('cfo)}\n            f"Cảnh báo', 'cfo)}\\n"            f"Cảnh báo')
js = js.replace('Không\n            f"Bất thường', 'Không\\n"            f"Bất thường')

with open('agents/eb_credit_agent.py', 'w', encoding='utf-8') as f:
    f.write(js)
