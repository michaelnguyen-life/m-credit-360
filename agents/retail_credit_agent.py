"""M-Credit360 Retail / Personal Credit Assessment Agent.

Deterministic retail-credit assessment toolkit for Hackathon / UAT.
It does NOT make an autonomous lending decision and does NOT encode official
MSB policy unless approved rules are explicitly provided in the request.
"""
from __future__ import annotations

import json, logging, math, os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Mapping

LOGGER = logging.getLogger("mcredit360.retail")

class AssessmentError(ValueError):
    pass

def dec(v: Any) -> Decimal | None:
    if v is None or v == "": return None
    if isinstance(v, bool): return None
    try:
        if isinstance(v, str):
            v=v.replace("₫","").replace("VND","").replace(",","").replace(" ","")
        return Decimal(str(v))
    except (InvalidOperation, ValueError): return None

def num(v: Decimal | None):
    if v is None: return None
    q=v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(q) if q == q.to_integral() else float(q)

def ratio(a: Decimal | None,b: Decimal | None):
    if a is None or b is None or b == 0: return None
    return a/b

def annuity_payment(principal: Decimal, annual_rate: Decimal, months: int) -> Decimal:
    if months <= 0: raise AssessmentError("loan.tenor_months must be > 0")
    if annual_rate < 0: raise AssessmentError("loan.annual_interest_rate cannot be negative")
    if annual_rate == 0: return principal/Decimal(months)
    r=annual_rate/Decimal(12)
    # annual_rate supplied as decimal e.g. 0.10
    factor=(Decimal(1)+r) ** months
    return principal*r*factor/(factor-Decimal(1))

DEFAULT_RULES={
    "max_dti": Decimal("0.55"),
    "min_disposable_income": Decimal("5000000"),
    "max_card_utilization": Decimal("0.80"),
    "max_unverified_income_share": Decimal("0.35"),
    "min_statement_months": Decimal("3"),
}

@dataclass
class RetailCreditAssessment:
    rules: dict[str, Decimal] = field(default_factory=lambda: dict(DEFAULT_RULES))

    def assess(self, payload: Mapping[str,Any]) -> dict[str,Any]:
        if not isinstance(payload, Mapping): raise AssessmentError("Payload must be a JSON object.")
        warnings=[]
        rules=dict(self.rules)
        for k,v in (payload.get("rules") or {}).items() if isinstance(payload.get("rules"),Mapping) else []:
            x=dec(v)
            if x is not None and x>=0: rules[str(k)]=x
        customer=dict(payload.get("customer") or {}) if isinstance(payload.get("customer"),Mapping) else {}
        income_items=payload.get("income",[]) or []
        if not isinstance(income_items,list): raise AssessmentError("income must be a list")
        verified=Decimal("0"); unverified=Decimal("0"); gross=Decimal("0")
        income_breakdown=[]
        for i,item in enumerate(income_items,1):
            if not isinstance(item,Mapping): continue
            amt=dec(item.get("monthly_amount"))
            if amt is None or amt<0:
                warnings.append(f"Ignored invalid income item {i}."); continue
            gross += amt
            status=str(item.get("verification_status","unverified")).lower()
            eligible_pct=dec(item.get("eligible_percent"))
            if eligible_pct is None: eligible_pct=Decimal("1") if status=="verified" else Decimal("0")
            eligible_pct=max(Decimal("0"), min(Decimal("1"),eligible_pct))
            eligible=amt*eligible_pct
            if status=="verified": verified += eligible
            else: unverified += eligible
            income_breakdown.append({"type":item.get("type"),"monthly_amount":num(amt),"verification_status":status,"eligible_percent":num(eligible_pct),"eligible_amount":num(eligible)})
        eligible_income=verified+unverified

        debts=payload.get("existing_debts",[]) or []
        if not isinstance(debts,list): raise AssessmentError("existing_debts must be a list")
        existing_monthly=Decimal("0"); debt_breakdown=[]
        for i,item in enumerate(debts,1):
            if not isinstance(item,Mapping): continue
            p=dec(item.get("monthly_payment")) or Decimal("0")
            if p<0: p=Decimal("0")
            existing_monthly += p
            debt_breakdown.append({"type":item.get("type"),"outstanding":num(dec(item.get("outstanding"))),"monthly_payment":num(p)})

        cards=payload.get("credit_cards",[]) or []
        card_flags=[]
        for c in cards if isinstance(cards,list) else []:
            if not isinstance(c,Mapping): continue
            bal=dec(c.get("balance")) or Decimal("0"); lim=dec(c.get("limit"))
            util=ratio(bal,lim)
            if util is not None and util>rules["max_card_utilization"]:
                card_flags.append({"code":"HIGH_CARD_UTILIZATION","severity":"medium","observed":num(util),"threshold":num(rules['max_card_utilization'])})

        loan=payload.get("loan",{}) if isinstance(payload.get("loan"),Mapping) else {}
        principal=dec(loan.get("amount")) or Decimal("0")
        annual=dec(loan.get("annual_interest_rate")) or Decimal("0")
        months=int(loan.get("tenor_months") or 0)
        new_payment=annuity_payment(principal,annual,months) if principal>0 and months>0 else Decimal("0")
        total_debt=existing_monthly+new_payment
        dti=ratio(total_debt,eligible_income)
        disposable=eligible_income-total_debt
        unverified_share=ratio(unverified,eligible_income) if eligible_income else None

        docs=payload.get("documents",{}) if isinstance(payload.get("documents"),Mapping) else {}
        missing=[]
        required=["identity","income_proof","cic"]
        if loan.get("secured"): required.append("collateral_documents")
        for key in required:
            if not docs.get(key): missing.append(key)

        flags=[]
        def add(code,title,triggered,severity,observed=None,threshold=None,evidence=""):
            flags.append({"code":code,"title":title,"triggered":bool(triggered),"severity":severity if triggered else "none","observed_value":num(observed) if isinstance(observed,Decimal) else observed,"threshold":num(threshold) if isinstance(threshold,Decimal) else threshold,"evidence":evidence})
        add("RF01_DTI","DTI vượt ngưỡng demo", dti is not None and dti>rules["max_dti"], "high", dti, rules["max_dti"], "Total monthly debt / eligible monthly income.")
        add("RF02_LOW_DISPOSABLE","Thu nhập tích lũy thấp", disposable<rules["min_disposable_income"], "high", disposable, rules["min_disposable_income"], "Eligible income minus monthly debt obligation.")
        add("RF03_UNVERIFIED_INCOME","Tỷ trọng thu nhập chưa xác minh cao", unverified_share is not None and unverified_share>rules["max_unverified_income_share"], "medium", unverified_share, rules["max_unverified_income_share"], "Share of eligible income derived from not-yet-verified sources.")
        flags.extend([{**x,"triggered":True,"title":"Mức sử dụng thẻ tín dụng cao","evidence":"Card balance / limit exceeds demo threshold."} for x in card_flags])
        if missing:
            flags.append({"code":"RF05_MISSING_DOCS","title":"Hồ sơ chưa đầy đủ","triggered":True,"severity":"medium","observed_value":len(missing),"threshold":0,"evidence":", ".join(missing)})

        trig=[f for f in flags if f.get("triggered")]
        sev={"none":0,"low":1,"medium":2,"high":3,"critical":4}
        m=max((sev.get(str(f.get("severity")),0) for f in trig),default=0)
        recommendation="PROCEED_FOR_HUMAN_REVIEW" if m<3 else "REQUIRES_CREDIT_OFFICER_REVIEW"
        if missing: recommendation="ADDITIONAL_DOCUMENTS_REQUIRED"
        profile={
            "schema_version":"1.0","assessment_id":str(payload.get("assessment_id") or f"RB-{datetime.now(timezone.utc):%Y%m%d%H%M%S}"),
            "assessed_at":datetime.now(timezone.utc).isoformat(),"data_classification":payload.get("data_classification","SYNTHETIC_OR_UAT"),
            "customer":customer,"income":{"gross_monthly_income":num(gross),"verified_eligible_income":num(verified),"unverified_eligible_income":num(unverified),"eligible_monthly_income":num(eligible_income),"breakdown":income_breakdown},
            "debt":{"existing_monthly_obligation":num(existing_monthly),"new_loan_estimated_payment":num(new_payment),"total_monthly_obligation":num(total_debt),"breakdown":debt_breakdown},
            "ratios":{"dti":num(dti),"disposable_income":num(disposable),"unverified_income_share":num(unverified_share)},
            "loan":dict(loan),"missing_documents":missing,"red_flags":flags,
            "preliminary_recommendation":{"outcome":recommendation,"is_automated_credit_decision":False,"human_in_the_loop":True},
            "rules_applied":{k:num(v) for k,v in rules.items()},"warnings":warnings,
        }
        profile["credit_memo"] = self.render_memo(profile)
        return profile

    @staticmethod
    def render_memo(p:Mapping[str,Any])->str:
        c=p['customer']; r=p['ratios']; i=p['income']; d=p['debt']
        flags=[f for f in p['red_flags'] if f.get('triggered')]
        lines=["# M-Credit360 — Personal Credit Memo",f"**Khách hàng:** {c.get('name') or 'Chưa cung cấp'}  ",f"**Customer ID:** {c.get('customer_id') or 'N/A'}  ",f"**Kết quả sơ bộ:** {p['preliminary_recommendation']['outcome']}","","## Khả năng trả nợ",f"- Thu nhập đủ điều kiện: {i.get('eligible_monthly_income')}",f"- Nghĩa vụ nợ hiện hữu: {d.get('existing_monthly_obligation')}",f"- Nghĩa vụ khoản vay mới ước tính: {d.get('new_loan_estimated_payment')}",f"- DTI: {r.get('dti')}",f"- Thu nhập tích lũy: {r.get('disposable_income')}","","## Điểm cần lưu ý"]
        lines += [f"- [{f['severity'].upper()}] {f['title']}: {f.get('evidence','')}" for f in flags] or ["- Không phát hiện red flag theo bộ quy tắc demo."]
        lines += ["","## Hồ sơ cần bổ sung"] + ([f"- {x}" for x in p['missing_documents']] or ["- Không có theo checklist demo."])
        lines += ["","## Disclaimer","Bộ quy tắc mặc định chỉ phục vụ Hackathon/UAT, không phải chính sách MSB chính thức. AI chuẩn bị. Con người quyết định."]
        return "\n".join(lines)+"\n"

class Handler(BaseHTTPRequestHandler):
    agent=RetailCreditAssessment()
    def do_GET(self):
        if self.path.rstrip('/')=='/health': self.send_json(200,{"status":"ok","agent":"retail-credit-assessment"})
        else: self.send_json(404,{"error":"Not found"})
    def do_POST(self):
        if self.path.rstrip('/') not in {'/invocations','/assess'}: return self.send_json(404,{"error":"Not found"})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<=0 or n>10_000_000: raise AssessmentError('Request body must be between 1 byte and 10 MB.')
            req=json.loads(self.rfile.read(n).decode('utf-8')); payload=req.get('input',req) if isinstance(req,dict) else req
            self.send_json(200,self.agent.assess(payload))
        except (AssessmentError,json.JSONDecodeError,UnicodeDecodeError) as e: self.send_json(400,{"error":str(e)})
        except Exception:
            LOGGER.exception('Unexpected assessment failure'); self.send_json(500,{"error":"Internal assessment error"})
    def send_json(self,status,body):
        b=json.dumps(body,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self,fmt,*args): LOGGER.info('%s - %s',self.address_string(),fmt%args)

def run_server():
    logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO')); port=int(os.getenv('PORT','8080')); LOGGER.info('Retail Credit Agent listening on %s',port); ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
if __name__=='__main__': run_server()
