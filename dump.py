import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
for i, line in enumerate(lines):
    if 'async function runEBAssessment' in line:
        start = i
        with open('out.txt', 'w', encoding='utf-8') as fw:
            fw.write('\n'.join(lines[start:start+250]))
        break
