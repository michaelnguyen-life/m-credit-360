import urllib.request, json

payload = {
    "customer": {"customer_id": "KH01", "name": "PHẠM THANH BÌNH"},
    "loan": {"amount": 450000000, "tenor_months": 48},
    "income": [{"monthly_amount": 2919000000, "eligible_percent": 0.08}],
    "existing_debts": [{"outstanding": 2700000000, "monthly_payment": 30000000}]
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    'http://localhost:8080/rb/export-memo-docx',
    data=data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as resp:
    print("HTTP Status:", resp.status)
    print("Content-Type:", resp.headers.get('Content-Type'))
    body = resp.read()
    print("Downloaded bytes:", len(body))
