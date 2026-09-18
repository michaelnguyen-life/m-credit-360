import urllib.request
try:
    req = urllib.request.Request("https://endpoint-9899d5b1-2190-47f7-a9c0-5cbc3070f609.agentbase-runtime.aiplatform.vngcloud.vn/", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8')
        with open('live_html.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Downloaded HTML, length: {len(html)}")
except Exception as e:
    print(e)
