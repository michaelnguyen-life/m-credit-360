import io
import re

with io.open('agents/eb_credit_agent.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('rreturn profile', 'return profile')

with io.open('agents/eb_credit_agent.py', 'w', encoding='utf-8') as f:
    f.write(text)
