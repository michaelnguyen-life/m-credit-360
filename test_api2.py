import json
import requests

payload = {
    "company": {"tax_id": "0311807068"},
    "financials": {
        "IS_REVENUE": 318000000000,
        "BS_TRADE_RECEIVABLES": 65000000000
    }
}
try:
    res = requests.post("http://localhost:8080/assess", json=payload)
    print("KEYS:", list(res.json().keys()))
    print("OSINT:", res.json().get('osint'))
    print("DEALS:", res.json().get('cross_sell_opportunities'))
except Exception as e:
    print(e)
