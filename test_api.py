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
    print(list(res.json().keys()))
except Exception as e:
    print(e)
