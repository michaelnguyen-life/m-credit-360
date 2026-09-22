import os, sys
sys.path.append('agents')
from rb_credit_memo_builder import RetailCreditMemoBuilder

builder = RetailCreditMemoBuilder()
res = builder.build({
    "customer": {"customer_id": "KH01", "name": "Phạm Thanh Bình"},
    "loan": {"amount": 450000000, "tenor_months": 48},
    "income": [{"monthly_amount": 2919000000, "eligible_percent": 0.08}],
    "existing_debts": [{"outstanding": 2700000000, "monthly_payment": 30000000}]
})

print("Result status:", res.get("status"))
print("Generated file:", res.get("file_name"))
print("File exists:", os.path.exists(res.get("file_path", "")))
print("File size:", os.path.getsize(res.get("file_path", "")))
