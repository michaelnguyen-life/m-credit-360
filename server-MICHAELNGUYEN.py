import os, sys, json, time, requests
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Setup agents path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
from eb_credit_agent import CreditAssessment
from retail_credit_agent import RetailCreditAssessment
from credit_memo_builder_agent import CreditMemoBuilder
from statement_analyzer_agent import StatementAnalyzer
from policy_eligibility_agent import PolicyEligibility

# GreenNode MaaS LLM Configuration
GREENNODE_MAAS_URL = os.environ.get(
    "GREENNODE_MAAS_URL",
    "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions"
)
GREENNODE_API_KEY = os.environ.get(
    "GREENNODE_API_KEY",
    "vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d"
)
GREENNODE_MODEL = "qwen/qwen3.6-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_ALPHA_PATH = os.path.join(BASE_DIR, "data_test", "1. CTY DAU TU GROUP (MOCK AN DANH)", "eb_credit_payload.json")
SAMPLE_BETA_PATH = os.path.join(BASE_DIR, "data_test", "2. CTY SAN XUAT XNK BETA (MOCK CHUAN CROSS-SELL)", "eb_credit_payload.json")
SAMPLE_RB_PATH = os.path.join(BASE_DIR, "data_test", "retail", "retail_tiktok_shop_sample.json")

app = FastAPI(
    title='M-Credit 360 All-in-One Super Agent',
    version='3.0-unified',
    description='Unified Credit Assessment Super Agent for MSB AI Hackathon 2026 (Team 22 - Hattrick)'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Mount static folder
static_dir = os.path.join(BASE_DIR, 'static')
if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')

@app.on_event("startup")
def startup_event():
    if os.environ.get("ENABLE_ZALO_BOT", "false").lower() in ["true", "1", "yes"]:
        try:
            import threading, zalo_bot_service
            t = threading.Thread(target=zalo_bot_service.run_service, daemon=True)
            t.start()
            print("[SERVER] Zalo Bot Gateway background thread started successfully!")
        except Exception as e:
            print(f"[SERVER] Failed to start Zalo Bot thread: {e}")

@app.get('/', response_class=HTMLResponse)
def web_portal():
    tmpl_path = os.path.join(BASE_DIR, 'templates', 'index.html')
    if os.path.exists(tmpl_path):
        with open(tmpl_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>M-Credit 360 All-in-One Super Agent Live on GreenNode AgentBase</h1>")

@app.get('/health')
@app.get('/ping')
def health_check():
    return {
        'status': 'healthy',
        'service': 'M-Credit 360 All-in-One Super Agent',
        'version': '3.0-unified',
        'team': 'Team 22 - Hattrick',
        'leader': 'Michael Nguyen (EB MSB)',
        'runtime': 'GreenNode AgentBase',
        'dual_channels': {
            'web_portal': 'active (GET /)',
            'zalo_bot_gateway': 'active (@bot.MaqROeGH)'
        },
        'capabilities': [
            'EB Enterprise Credit Assessment (NWC, WCR, DSCR, ICR, Rule 5D, Out-flow Skeleton)',
            'RB Retail & TikTok Shop Credit Assessment (DTI, Card Utilization, Disposable Income)',
            'MB02a Master Credit Memo Builder (.docx, 8 Sections, 21 Tables)',
            'Statement Analyzer (Rule 5D Cross-sell & Out-flow)',
            'Policy Eligibility Engine',
            'GreenNode MaaS Cloud LLM (qwen/qwen3.6-flash)'
        ]
    }

@app.post('/zalo-webhook')
async def zalo_webhook(request: Request):
    try:
        data = await request.json()
        import zalo_bot_service
        msg = data.get('result', {}).get('message')
        if msg:
            zalo_bot_service.process_incoming_message(msg)
        return {'status': 'ok'}
    except Exception as e:
        return {'status': 'error', 'detail': str(e)}

@app.post('/invocations')
async def invoke_agent(request: Request):
    """
    Standard Single Unified Endpoint for GreenNode AgentBase.
    Automatically handles and routes:
    1. Corporate / Enterprise Banking (EB)
    2. Retail / Personal Banking (RB)
    3. Credit Memo MB02a (.docx) Builder
    4. Statement Analyzer
    5. Policy Eligibility
    """
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    action = body.get('action')
    payload = body.get('payload', body)
    if isinstance(payload, dict) and 'action' in payload and not action:
        action = payload.get('action')

    # 1. Explicit Action Handling
    if action in ['build_docx', 'build_memo', 'mb02a']:
        builder = CreditMemoBuilder(output_dir=os.path.join(BASE_DIR, 'output_memos'))
        return builder.build(payload)
        
    if action == 'analyze_statement':
        txs = payload.get('transactions', [])
        return StatementAnalyzer(transactions=txs).analyze()
        
    if action in ['evaluate_policy', 'policy']:
        return PolicyEligibility().evaluate(payload)
        
    if action in ['rb_assess', 'retail', 'personal']:
        return RetailCreditAssessment().assess(payload)
        
    if action in ['eb_assess', 'corporate', 'enterprise']:
        return CreditAssessment().assess(payload)

    # 2. Intelligent Auto-Routing
    is_rb = (
        payload.get('segment') in ['RB', 'retail', 'personal', 'individual_business_owner'] or
        'applicant' in payload or
        ('customer' in payload and isinstance(payload['customer'], dict) and (
            payload['customer'].get('segment') in ['individual', 'individual_business_owner'] or
            'business_channel' in payload['customer'] or
            'customer_id' in payload['customer']
        )) or
        ('income' in payload and isinstance(payload['income'], list)) or
        'existing_debts' in payload or
        'credit_cards' in payload
    )

    if is_rb:
        try:
            return RetailCreditAssessment().assess(payload)
        except Exception:
            return CreditAssessment().assess(payload)
    else:
        return CreditAssessment().assess(payload)

@app.post('/assess')
def assess_credit(payload: dict):
    """Enterprise Credit Assessment Endpoint"""
    try:
        return CreditAssessment().assess(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/rb/assess')
def assess_retail_credit(payload: dict):
    """Retail Credit Assessment Endpoint"""
    try:
        return RetailCreditAssessment().assess(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/policy/evaluate')
def evaluate_policy(payload: dict):
    """Policy Eligibility Endpoint"""
    try:
        return PolicyEligibility().evaluate(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/build-memo-docx')
def build_memo_docx(payload: dict):
    """Generates MSB MB02a DOCX Credit Proposal and returns as download"""
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

@app.post('/api/chat')
async def api_chat(request: Request):
    """GreenNode MaaS Cloud LLM Credit Advisory Endpoint"""
    try:
        data = await request.json()
        user_msg = data.get('message', '').strip()
        if not user_msg:
            return {'reply': 'Xin chào Team 22 Hackathon & Ban Giám Khảo! Tôi là AI Chuyên gia Tín dụng MSB (Team 22). Bạn có thể hỏi bất kỳ câu hỏi nào về quy chuẩn BCTC, thẩm định rủi ro, phân tích dòng tiền Rule 5D, hoặc chính sách bán chéo QĐ 039.'}
            
        system_prompt = (
            "Bạn là M-CREDIT 360 AI - Chuyên gia Thẩm định Tín dụng Cấp cao của Ngân hàng MSB (Team 22 Hattrick).\n"
            "Lãnh đạo: Michael Nguyên (Giám đốc KHDN EB MSB).\n"
            "QUY TẮC:\n"
            "1. Tuyệt đối KHÔNG viết tắt trơ trọi các chỉ số NWC, DSCR, ICR, WCR mà phải luôn ghi rõ TÊN TIẾNG VIỆT ĐẦY ĐỦ kèm công thức và ý nghĩa thẩm định MSB.\n"
            "2. Phân tích bám sát khẩu vị rủi ro MSB: Vốn lưu động ròng NWC >= 0, Hệ số DSCR >= 1.0x, Hệ số ICR >= 1.5x, Rule 5D dòng tiền về MSB >= 80% Có 131.\n"
            "3. Khi người dùng mới chỉ gửi thông tin tên công ty, MST, địa chỉ mà CHƯA có số liệu tài chính cụ thể, hãy xác nhận thông tin đã nhận và BẮT BUỘC dùng đúng câu: '* Lưu ý : Để xuất ngay BÁO CÁO SƠ BỘ, tôi cần bổ sung bộ dữ liệu tài chính thực tế của công ty trong 12–24 tháng gần nhất. Vui lòng cung cấp'.\n"
            "4. Ngôn ngữ đĩnh đạc, chuyên nghiệp, sắc bén, đi thẳng vào bản chất tài chính."
        )
        body = {
            "model": GREENNODE_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            "temperature": 0.4,
            "max_tokens": 1000
        }
        headers = {
            "Authorization": f"Bearer {GREENNODE_API_KEY}",
            "Content-Type": "application/json"
        }
        t0 = time.time()
        r = requests.post(GREENNODE_MAAS_URL, json=body, headers=headers, timeout=30)
        elapsed = time.time() - t0
        if r.status_code == 200:
            res_json = r.json()
            content = res_json["choices"][0]["message"]["content"]
            import re
            target_notice = "* Lưu ý : Để xuất ngay BÁO CÁO SƠ BỘ, tôi cần bổ sung bộ dữ liệu tài chính thực tế của công ty trong 12–24 tháng gần nhất. Vui lòng cung cấp"
            content = re.sub(
                r"[⚠️\*•\s]*Lưu ý[^\n:]*:\s*Để xuất ngay BÁO CÁO[^\n]*?tôi cần bổ sung bộ dữ liệu tài chính[^\n]*?Vui lòng cung cấp:?",
                target_notice,
                content,
                flags=re.IGNORECASE
            )
            return {'reply': content, 'elapsed': elapsed}
        else:
            return {'reply': f'Hệ thống GreenNode MaaS AI phản hồi lỗi: {r.status_code}'}
    except Exception as e:
        return {'reply': f'Lỗi kết nối AI MaaS Cloud: {str(e)}'}

@app.get('/api/sample/eb/alpha')
def get_sample_alpha():
    if os.path.exists(SAMPLE_ALPHA_PATH):
        with open(SAMPLE_ALPHA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Sample Alpha not found")

@app.get('/api/sample/eb/beta')
def get_sample_beta():
    if os.path.exists(SAMPLE_BETA_PATH):
        with open(SAMPLE_BETA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Sample Beta not found")

@app.get('/api/sample/rb/tiktok')
def get_sample_rb():
    if os.path.exists(SAMPLE_RB_PATH):
        with open(SAMPLE_RB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Sample RB not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', host='0.0.0.0', port=8080, reload=False)
