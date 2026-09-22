import io
with io.open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('function handleFileSelect(e)')
end = html.find('function openExtractionReview()')
print(html[start:end])
