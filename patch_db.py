# -*- coding: utf-8 -*-
import codecs
import re

content = codecs.open('server.py', 'r', 'utf-8').read()

target = '''@app.get("/api/lookup-mst")'''
replacement = '''import json
import os

DB_FILE = os.path.join(BASE_DIR, "customer_db.json")

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except:
        pass

from pydantic import BaseModel
class CustomerSavePayload(BaseModel):
    mst: str
    name: str
    financials: dict
    filename: str

@app.post("/api/customer/save")
def save_customer(payload: CustomerSavePayload):
    db = load_db()
    db[payload.mst] = {
        "name": payload.name,
        "financials": payload.financials,
        "filename": payload.filename
    }
    save_db(db)
    return {"success": True}

@app.get("/api/customer/load")
def load_customer(mst: str):
    db = load_db()
    if mst in db:
        return {"success": True, "data": db[mst]}
    return {"success": False}

@app.get("/api/lookup-mst")'''

if target in content:
    content = content.replace(target, replacement)
    codecs.open('server.py', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
