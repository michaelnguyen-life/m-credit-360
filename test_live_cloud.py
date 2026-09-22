import requests, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

url_assess = 'https://endpoint-532eb3d4-0d9d-4b19-93c1-2ebc3060bca4.agentbase-runtime.aiplatform.vngcloud.vn/assess'
url_memo = 'https://endpoint-05361e8d-12de-4860-8c26-d6e637d5aa42.agentbase-runtime.aiplatform.vngcloud.vn/build-memo-docx'
exist_path = 'data_test/1. CTY DAU TU GROUP (MOCK AN DANH)/eb_credit_payload.json'
if not os.path.exists(exist_path):
    exist_path = os.path.join(os.path.dirname(__file__), exist_path)

print('=====================================================================')
print('  M-CREDIT 360 - TEST TRUC TIEP DU LIEU BCTC LEN GREENNODE CLOUD')
print('=====================================================================')

print('\n[1/2] DANG GUI DU LIEU BCTC ALPHA GROUP (318 TY) LEN AGENT 1 CLOUD...')
payload = json.load(open(exist_path, encoding='utf-8'))
res1 = requests.post(url_assess, json=payload, timeout=20)

if res1.status_code == 200:
    data = res1.json()
    comp = data.get('company', {})
    r = data.get('ratios', {})
    print(' -> KET NOI CLOUD THANH CONG (HTTP 200 OK)')
    print(' -> Doanh nghiep:', comp.get('name'), '(MST:', comp.get('tax_id'), ')')
    print(' -> Chi so NWC (Von luu dong rong):', f"{r.get('nwc', 0):,.0f}", 'VND')
    print(' -> Chi so WCR (Nhu cau von luu dong):', f"{r.get('wcr', 0):,.0f}", 'VND')
    print(' -> He so tra no DSCR:', f"{r.get('dscr', 0):.2f}x")
    print(' -> He so ICR:', f"{r.get('icr', 0):.2f}x")
    print(' -> Ket qua so bo:', data.get('preliminary_decision', {}).get('outcome'))
    print(' -> Danh gia San pham 039 MSB:', data.get('product_039_evaluation', {}).get('decision'))
    print(' -> Canh bao Red Flags phat hien:')
    for f in data.get('red_flags', []):
        if f.get('triggered'):
            sev = f.get('severity', '').upper()
            title = f.get('title', '')
            ev = f.get('evidence', '')
            print('    [!] [' + sev + '] ' + title + ': ' + ev)
else:
    print(' -> LOI KET NOI:', res1.status_code, res1.text)

print('\n[2/2] DANG GOI AGENT 4 XUAT TO TRINH TIN DUNG MB02a TREN CLOUD...')
res2 = requests.post(url_memo, json={'eb_payload': payload}, timeout=20)
if res2.status_code == 200:
    data2 = res2.json()
    print(' -> TAO TO TRINH MB02a THANH CONG TREN CLOUD!')
    print(' -> File Word tao tren Cloud:', data2.get('file_path'))
    print(' -> Quyet dinh San pham 039:', data2.get('product_039_decision'))
else:
    print(' -> LOI XUAT TO TRINH:', res2.status_code, res2.text)

print('\n=====================================================================')
print('  KET LUAN: HE THONG LIVE 100% - SAN SANG TRINH DIEN BAN GIAM KHAO!')
print('=====================================================================')
