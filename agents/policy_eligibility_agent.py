"""Configurable policy eligibility engine for M-Credit360 Retail.

Rules are supplied by the caller. This module intentionally ships with DEMO
rules only and does not claim to reproduce QĐ.RB.129 or any other MSB policy.
"""
from __future__ import annotations
import json, os, logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http import HTTPStatus
from typing import Any, Mapping

class PolicyError(ValueError): pass

def get_path(obj:Mapping[str,Any], path:str):
    cur:Any=obj
    for part in path.split('.'):
        if not isinstance(cur,Mapping) or part not in cur: return None
        cur=cur[part]
    return cur

def evaluate_condition(actual, op, expected):
    if op=='exists': return actual is not None
    if op=='eq': return actual==expected
    if op=='ne': return actual!=expected
    try:
        if op=='gte': return actual>=expected
        if op=='gt': return actual>expected
        if op=='lte': return actual<=expected
        if op=='lt': return actual<expected
        if op=='in': return actual in expected
    except TypeError: return False
    raise PolicyError(f'Unsupported operator: {op}')

class PolicyEligibility:
    def evaluate(self,payload:Mapping[str,Any]):
        case=payload.get('case',{}) if isinstance(payload.get('case'),Mapping) else {}
        rules=payload.get('policy_rules',[]) or []
        if not isinstance(rules,list): raise PolicyError('policy_rules must be a list')
        results=[]
        for idx,r in enumerate(rules,1):
            if not isinstance(r,Mapping): continue
            field=str(r.get('field','')); op=str(r.get('op','exists')); expected=r.get('value'); actual=get_path(case,field) if field else None
            if actual is None and op!='exists': status='NEED_MORE_DATA'; passed=None
            else:
                passed=evaluate_condition(actual,op,expected); status='PASS' if passed else 'FAIL'
            results.append({'rule_id':r.get('rule_id',f'R{idx:02d}'),'title':r.get('title',field),'field':field,'operator':op,'expected':expected,'actual':actual,'status':status,'evidence':r.get('evidence_note'),'source_reference':r.get('source_reference')})
        counts={s:sum(1 for x in results if x['status']==s) for s in ['PASS','FAIL','NEED_MORE_DATA']}
        if counts['FAIL']: outcome='POLICY_MISMATCH_REQUIRES_REVIEW'
        elif counts['NEED_MORE_DATA']: outcome='CONDITIONAL_MATCH'
        else: outcome='MATCH_SUBJECT_TO_HUMAN_REVIEW'
        return {'policy_name':payload.get('policy_name','DEMO POLICY'),'policy_version':payload.get('policy_version'),'outcome':outcome,'summary':counts,'results':results,'is_automated_credit_decision':False,'disclaimer':'Rules must be populated from an approved policy source before UAT/production. AI prepares. Human decides.'}

class Handler(BaseHTTPRequestHandler):
    agent=PolicyEligibility()
    def do_GET(self):
        self.send_json(200,{'status':'ok','agent':'retail-policy-eligibility'}) if self.path.rstrip('/')=='/health' else self.send_json(404,{'error':'Not found'})
    def do_POST(self):
        if self.path.rstrip('/') not in {'/invocations','/evaluate'}: return self.send_json(404,{'error':'Not found'})
        try:
            n=int(self.headers.get('Content-Length','0')); req=json.loads(self.rfile.read(n).decode()); payload=req.get('input',req) if isinstance(req,dict) else req; self.send_json(200,self.agent.evaluate(payload))
        except (PolicyError,json.JSONDecodeError) as e: self.send_json(400,{'error':str(e)})
    def send_json(self,s,b):
        raw=json.dumps(b,ensure_ascii=False).encode(); self.send_response(s); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def log_message(self,fmt,*args): pass

def run_server(): ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8080'))),Handler).serve_forever()
if __name__=='__main__': run_server()
