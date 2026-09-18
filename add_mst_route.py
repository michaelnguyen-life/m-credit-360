# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('server.py', 'r', 'utf-8').read()

target = '''@app.on_event("startup")'''

replacement = '''import requests

@app.get("/api/lookup-mst")
def lookup_mst(mst: str):
    try:
        res = requests.get(f'https://api.vietqr.io/v2/business/{mst}', timeout=10)
        data = res.json()
        if data.get('code') == '00' and 'data' in data and data['data']:
            return {"success": True, "name": data['data'].get('name', '')}
        return {"success": False, "error": "Không tìm thấy doanh nghiệp"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.on_event("startup")'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('server.py', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
