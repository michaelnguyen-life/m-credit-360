import io
import json

with io.open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

# Add save/load endpoints
save_load_endpoints = '''
# ------------------ SAVE/LOAD LOGIC ------------------
DB_FILE = os.path.join(BASE_DIR, "database.json")

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.post('/api/save-eb')
def save_eb(payload: dict):
    mst = payload.get("company", {}).get("tax_id", "")
    if not mst:
        raise HTTPException(status_code=400, detail="Missing tax_id")
    db = load_db()
    db[mst] = payload
    save_db(db)
    return {"status": "success", "message": "Saved"}

@app.get('/api/load-eb/{mst}')
def load_eb(mst: str):
    db = load_db()
    if mst in db:
        return db[mst]
    raise HTTPException(status_code=404, detail="Not found")
# -----------------------------------------------------
'''

# Find @app.get('/api/sample/eb/{sample_id}')
target = "@app.get('/api/sample/eb/{sample_id}')"
server = server.replace(target, save_load_endpoints + "\n" + target)

with io.open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
