import urllib.request
import json
import threading
import uvicorn
from fastapi import FastAPI
import time
import sys

def run_tests():
    time.sleep(2) # wait for server
    try:
        # Test 1: /assess
        payload = {
            'assessment_id': 'EB-QA-TEST',
            'company': {'tax_id': '0311807068', 'name': 'QA Corp'},
            'financials': {'IS_REVENUE': 318000000000, 'BS_CURRENT_ASSETS': 120000000000, 'BS_CURRENT_LIABILITIES': 145000000000}
        }
        req = urllib.request.Request('http://127.0.0.1:8080/assess', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode('utf-8'))
            assert 'preliminary_decision' in data
            print("PASS: /assess endpoint works")

        # Test 2: /build-memo-docx
        req2 = urllib.request.Request('http://127.0.0.1:8080/build-memo-docx', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req2) as res2:
            assert res2.status == 200
            assert res2.headers.get('content-type') == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            content_disposition = res2.headers.get('content-disposition')
            assert content_disposition and 'attachment' in content_disposition
            blob = res2.read()
            assert len(blob) > 0
            print("PASS: /build-memo-docx endpoint works and returns DOCX")
            
    except Exception as e:
        print("FAIL:", str(e))
        import traceback
        traceback.print_exc()

import subprocess
import os

print("Starting backend for QA...")
proc = subprocess.Popen([sys.executable, "server.py"], cwd="c:/Users/finan/OneDrive/Documents/02. DU AN AI & CONG NGHE/THUONG THUONG AI/32_HATTRICK/NOP BAI/M_CREDIT_360_FINAL_ALL_IN_ONE")
run_tests()
proc.terminate()
print("QA testing finished.")
