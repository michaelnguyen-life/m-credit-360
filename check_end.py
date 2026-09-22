import io
with io.open('agents/eb_credit_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'profile["one_page_credit_memo"]' in line:
        print(''.join(lines[i:i+5]))
