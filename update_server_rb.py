import io

with io.open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add import
old_import = "from credit_memo_builder_agent import CreditMemoBuilder"
new_import = "from credit_memo_builder_agent import CreditMemoBuilder\nfrom rb_credit_memo_builder import RetailCreditMemoBuilder"

if old_import in code:
    code = code.replace(old_import, new_import)
    print("Added RetailCreditMemoBuilder import")

# 2. Add endpoint after build_memo_docx
old_endpoint = """@app.post('/build-memo-docx')
def build_memo_docx(payload: dict):
    \"\"\"Generates MSB MB02a DOCX Credit Proposal and returns as download\"\"\"
    try:
        builder = CreditMemoBuilder(output_dir=os.path.join(BASE_DIR, 'output_memos'))
        res = builder.build(payload)
        fp = res.get('file_path')
        if fp and os.path.exists(fp):
            return FileResponse(
                path=fp,
                filename=os.path.basename(fp),
                media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))"""

new_endpoint = """@app.post('/build-memo-docx')
def build_memo_docx(payload: dict):
    \"\"\"Generates MSB MB02a DOCX Credit Proposal and returns as download\"\"\"
    try:
        builder = CreditMemoBuilder(output_dir=os.path.join(BASE_DIR, 'output_memos'))
        res = builder.build(payload)
        fp = res.get('file_path')
        if fp and os.path.exists(fp):
            return FileResponse(
                path=fp,
                filename=os.path.basename(fp),
                media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/rb/build-memo-docx')
@app.post('/rb/export-memo-docx')
def build_rb_memo_docx(payload: dict):
    \"\"\"Generates MSB MB01A DOCX Personal/Retail Credit Proposal and returns as download\"\"\"
    try:
        builder = RetailCreditMemoBuilder(output_dir=os.path.join(BASE_DIR, 'output_memos'))
        res = builder.build(payload)
        fp = res.get('file_path')
        if fp and os.path.exists(fp):
            return FileResponse(
                path=fp,
                filename=os.path.basename(fp),
                media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))"""

if old_endpoint in code:
    code = code.replace(old_endpoint, new_endpoint)
    print("Added /rb/build-memo-docx endpoint")

# Also add routing in /invocations
old_invoc = "if action in ['build_docx', 'build_memo', 'mb02a']:"
new_invoc = """if action in ['build_rb_docx', 'build_rb_memo', 'mb01a']:
        builder = RetailCreditMemoBuilder(output_dir=os.path.join(BASE_DIR, 'output_memos'))
        return builder.build(payload)
        
    if action in ['build_docx', 'build_memo', 'mb02a']:"""

if old_invoc in code:
    code = code.replace(old_invoc, new_invoc)
    print("Added invocation action for mb01a")

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated server.py successfully!")
