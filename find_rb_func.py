import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('runRBAssessment')
if idx != -1:
    print('Found runRBAssessment at:', idx)
    print(html[idx:idx+1200])
else:
    print('runRBAssessment NOT defined')
