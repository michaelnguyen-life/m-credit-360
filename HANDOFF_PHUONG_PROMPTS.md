# Tổng hợp System Prompts & Templates các Agent (Phiên bản Code)

## File: eb_credit_agent.py
### Đoạn Prompt/Template 1
`	ext
M-Credit 360 Enterprise Credit Assessment Agent.

Input is a JSON payload containing MSB-coded financial data.  The default
mapping is deliberately configurable because an approved MSB data dictionary
must be used before production credit decisions are made.
`

### Đoạn Prompt/Template 2
`	ext
Convert common Vietnamese amount formats to an integer VND amount.

    This is intentionally deterministic: unsupported wording returns None
    instead of allowing a model or heuristic to infer a financial value.
`

### Đoạn Prompt/Template 3
`	ext
<div class="flex justify-between items-center"><span class="truncate pr-2">• Cung cấp VLXD</span><span class="font-mono font-bold text-slate-800">12,5 Tỷ</span></div>
                    <div class="flex justify-between items-center"><span class="truncate pr-2">• Thi công Trạm Y tế</span><span class="font-mono font-bold text-slate-800">8,2 Tỷ</span></div>
                    <div class="flex justify-between items-center"><span class="truncate pr-2">• Cải tạo Trường</span><span class="font-mono font-bold text-slate-800">4,1 Tỷ</span></div>
`

## File: retail_credit_agent.py
### Đoạn Prompt/Template 1
`	ext
M-Credit360 Retail / Personal Credit Assessment Agent.

Deterministic retail-credit assessment toolkit for Hackathon / UAT.
It does NOT make an autonomous lending decision and does NOT encode official
MSB policy unless approved rules are explicitly provided in the request.
`

## File: credit_memo_builder_agent.py
*Không tìm thấy text dài nào > 200 ký tự.*

## File: statement_analyzer_agent.py
*Không tìm thấy text dài nào > 200 ký tự.*

## File: policy_eligibility_agent.py
### Đoạn Prompt/Template 1
`	ext
Configurable policy eligibility engine for M-Credit360 Retail.

Rules are supplied by the caller. This module intentionally ships with DEMO
rules only and does not claim to reproduce QĐ.RB.129 or any other MSB policy.
`

## File: rb_credit_memo_builder.py
### Đoạn Prompt/Template 1
`	ext
M-Insight 360 Retail Credit Proposal Builder (MB01A/QT.RR.038).

Fills official MSB MB01A credit application and assessment proposal from RB payload data.
Template: MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx
`

## File: server.py
### Đoạn Prompt/Template 1
`	ext
Standard Single Unified Endpoint for GreenNode AgentBase.
    Automatically handles and routes:
    1. SME Banking (EB)
    2. Retail / Personal Banking (RB)
    3. Credit Memo MB02a (.docx) Builder
    4. Statement Analyzer
    5. Policy Eligibility
`

### Đoạn Prompt/Template 2
`	ext
Xin chào Team 22 Hackathon & Ban Giám Khảo! Tôi là AI Chuyên gia Tín dụng MSB (Team 22). Bạn có thể hỏi bất kỳ câu hỏi nào về quy chuẩn BCTC, thẩm định rủi ro, phân tích dòng tiền Rule 5D, hoặc chính sách bán chéo QĐ 039.
`

### Đoạn Prompt/Template 3
`	ext
Bạn là M-CREDIT 360 AI - Chuyên gia Thẩm định Tín dụng Cấp cao của Ngân hàng MSB (Team 22 Hattrick).
Lãnh đạo: Michael Nguyên (Giám đốc KHDN EB MSB).
QUY TẮC:
1. Tuyệt đối KHÔNG viết tắt trơ trọi các chỉ số NWC, DSCR, ICR, WCR mà phải luôn ghi rõ TÊN TIẾNG VIỆT ĐẦY ĐỦ kèm công thức và ý nghĩa thẩm định MSB.
2. Phân tích bám sát khẩu vị rủi ro MSB: Vốn lưu động ròng NWC >= 0, Hệ số DSCR >= 1.0x, Hệ số ICR >= 1.5x, Rule 5D dòng tiền về MSB >= 80% Có 131.
3. Khi người dùng mới chỉ gửi thông tin tên công ty, MST, địa chỉ mà CHƯA có số liệu tài chính cụ thể, hãy xác nhận thông tin đã nhận và BẮT BUỘC dùng đúng câu: '* Lưu ý : Để xuất ngay BÁO CÁO SƠ BỘ, tôi cần bổ sung bộ dữ liệu tài chính thực tế của công ty trong 12–24 tháng gần nhất. Vui lòng cung cấp'.
4. Ngôn ngữ đĩnh đạc, chuyên nghiệp, sắc bén, đi thẳng vào bản chất tài chính.
`

### Đoạn Prompt/Template 4
`	ext
{
  "assessment_id": "EB-ALPHA-2025-001",
  "company": {
    "name": "CÔNG TY CỔ PHẦN TẬP ĐOÀN ĐẦU TƯ ALPHA (MOCK AN DANH)",
    "tax_id": "0318999888",
    "cif": "CIF-ALPHA-2025",
    "industry": "Đầu tư & Xây lắp Bất động sản / Thương mại",
    "operating_years": 8,
    "legal_rep": "NGUYỄN VĂN ALPHA",
    "customer_status": "Mới",
    "customer_segment": "SME",
    "registered_address": "Số 12, Nguyễn Huệ, Q.1, TP.HCM"
  },
  "legal": {
    "registration_number": "0318999888",
    "registration_date": "15/03/2017",
    "registration_place": "Sở KH&ĐT TP.HCM",
    "charter_capital": 500000000000,
    "paid_capital": 500000000000,
    "legal_rep_id": "079200012345",
    "legal_rep_id_date": "15/06/2021",
    "industry_level3": "Xây dựng công trình",
    "industry_level5": "Xây lắp công trình dân dụng và công nghiệp",
    "risk_sector": "Bất động sản"
  },
  "reporting_period": "FY2025",
  "currency": "VND",
  "financials": {
    "BS_CURRENT_ASSETS": 293369838619,
    "BS_CURRENT_LIABILITIES": 165307940854,
    "BS_TRADE_RECEIVABLES": 1030523666,
    "BS_INVENTORY": 13676836829,
    "BS_TRADE_PAYABLES": 1440085191,
    "BS_SHORT_TERM_DEBT": 78810636239,
    "BS_TOTAL_LIABILITIES": 289109192531,
    "BS_EQUITY": 580965107518,
    "BS_TOTAL_ASSETS": 870074300049,
    "BS_LONG_TERM_DEBT": 0,
    "IS_REVENUE": 90105893754,
    "IS_GROSS_PROFIT": 16764962136,
    "IS_EBIT": 12405554008,
    "IS_INTEREST_EXPENSE": 8579629925,
    "IS_NET_PROFIT": 23267766,
    "CF_OPERATING_CASH_FLOW": 8624346207,
    "CF_INVESTING_CASH_FLOW": -3920000000,
    "CF_FINANCING_CASH_FLOW": -4105345786,
    "PRINCIPAL_DUE": 15000000000
  },
  "financial_history": [
    {
      "period": "FY2023",
      "financials": {
        "IS_REVENUE": 75000000000,
        "BS_TOTAL_ASSETS": 750000000000,
        "BS_CURRENT_LIABILITIES": 140000000000,
        "BS_LONG_TERM_DEBT": 0,
        "BS_EQUITY": 520000000000,
        "IS_GROSS_PROFIT": 13000000000,
        "IS_EBIT": 9500000000,
        "IS_INTEREST_EXPENSE": 6000000000,
        "IS_NET_PROFIT": 1500000000,
        "CF_OPERATING_CASH_FLOW": 5000000000
      }
    },
    {
      "period": "FY2024",
      "financials": {
        "IS_REVENUE": 82000000000,
        "BS_TOTAL_ASSETS": 810000000000,
        "BS_CURRENT_LIABILITIES": 155000000000,
        "BS_LONG_TERM_DEBT": 0,
        "BS_EQUITY": 555000000000,
        "IS_GROSS_PROFIT": 15000000000,
        "IS_EBIT": 11000000000,
        "IS_INTEREST_EXPENSE": 7500000000,
        "IS_NET_PROFIT": 800000000,
        "CF_OPERATING_CASH_FLOW": 6800000000
      }
    }
  ],
  "dsp": {
    "revenue": 89500000000,
    "trade_receivables": 1050000000
  },
  "cic": {
    "msb_short_term_debt": 0,
    "other_short_term_debt": 78810636239,
    "msb_long_term_debt": 0,
    "other_long_term_debt": 0,
    "debt_group": "Nhóm 1",
    "payment_history": "Tốt"
  },
  "collateral": [
    {
      "type": "Bất động sản",
      "name": "Đất nền dự án Alpha Garden",
      "owner": "CTCP Tập đoàn Đầu tư Alpha",
      "relationship": "Tài sản của KH",
      "value": 300000000000,
      "allocation_ratio": 0.5
    }
  ],
  "credit_terms": {
    "short_term_limit": 15000000000,
    "trade_finance_limit": 5000000000,
    "guarantee_limit": 3000000000,
    "tenor": "12 tháng",
    "interest_rate": "8.5%/năm",
    "deposit_ratio": "10%",
    "collateral": "Bất động sản (150% giá trị HMTD)",
    "disbursement_conditions": "Giải ngân từng lần theo tiến độ HDDR; kiểm soát dòng tiền thu về",
    "post_disbursement_conditions": "Báo cáo tài chính quý; giám sát dòng tiền 6 tháng/lần",
    "proposed_limit": 15000000000
  },
  "supply_chain": {
    "top_suppliers": [
      {"name": "CTCP VLXD SÀI GÒN", "amount": 4500000000, "ratio": 0.35, "payment_terms": "30 ngày", "relationship_years": 5},
      {"name": "CTCP THÉP HÒA PHÁT", "amount": 3200000000, "ratio": 0.25, "payment_terms": "45 ngày", "relationship_years": 4},
      {"name": "CTCP XÂY DỰNG COTECC", "amount": 1800000000, "ratio": 0.14, "payment_terms": "30 ngày", "relationship_years": 3},
      {"name": "CTCP VẬT TƯ ĐIỆN CƠ ĐIỆN", "amount": 1200000000, "ratio": 0.09, "payment_terms": "15 ngày", "relationship_years": 2},
      {"name": "CTCP NHỰA BÌNH MINH", "amount": 800000000, "ratio": 0.06, "payment_terms": "30 ngày", "relationship_years": 3}
    ],
    "top_buyers": [
      {"name": "CTCP ĐẦU TƯ BETA", "amount": 20000000000, "ratio": 0.22, "payment_terms": "60 ngày", "relationship_years": 3},
      {"name": "CTCP BẤT ĐỘNG SẢN GAMMA", "amount": 15000000000, "ratio": 0.17, "payment_terms": "45 ngày", "relationship_years": 2},
      {"name": "CTCP XÂY DỰNG DELTA", "amount": 12000000000, "ratio": 0.13, "payment_terms": "30 ngày", "relationship_years": 4},
      {"name": "CTCP ĐẦU TƯ EPSILON", "amount": 8000000000, "ratio": 0.09, "payment_terms": "60 ngày", "relationship_years": 1},
      {"name": "CTCP NHÀ ĐẤT ZETA", "amount": 6000000000, "ratio": 0.07, "payment_terms": "45 ngày", "relationship_years": 2}
    ]
  },
  "statement_analysis": {
    "total_inflow": 18620000000000,
    "total_outflow": 18580000000000,
    "average_monthly_balance": 15000000000,
    "months_analyzed": 12,
    "anomalies": [
      {
        "code": "ANM01_LARGE_CASH_WITHDRAWAL",
        "title": "Rút tiền mặt lớn",
        "triggered": true,
        "severity": "high",
        "count": 3,
        "total_amount": 50000000000,
        "evidence": "3 lần rút tiền mặt > 10 tỷ trong 12 tháng, tổng 50 tỷ"
      },
      {
        "code": "ANM02_RAPID_MOVEMENT",
        "title": "Dòng tiền ra-vào nhanh (round-trip 24h)",
        "triggered": true,
        "severity": "medium",
        "count": 7,
        "total_amount": 35000000000,
        "evidence": "7 cặp giao dịch ra-vào trong 24h, tổng 35 tỷ"
      },
      {
        "code": "ANM03_ROUND_AMOUNT",
        "title": "Số tiền chẵn (bội số 100 triệu)",
        "triggered": true,
        "severity": "low",
        "count": 15,
        "total_amount": 45000000000,
        "evidence": "15 giao dịch số chẵn, tổng 45 tỷ"
      },
      {
        "code": "ANM04_AFTER_HOURS",
        "title": "Giao dịch ngoài giờ hành chính (23h-05h)",
        "triggered": true,
        "severity": "medium",
        "count": 5,
        "total_amount": 12000000000,
        "evidence": "5 giao dịch ngoài giờ, tổng 12 tỷ"
      },
      {
        "code": "ANM05_SENSITIVE_KEYWORDS",
        "title": "Từ khóa nhạy cảm (vay/trả nợ/cầm đồ/crypto)",
        "triggered": false,
        "severity": "none",
        "count": 0,
        "total_amount": 0,
        "evidence": "Không phát hiện giao dịch chứa từ khóa nhạy cảm"
      }
    ]
  },
  "product_039": {
    "customer_operating_years": 8,
    "customer_equity": 580965107518,
    "buyer_name": "CÔNG TY CP KHÁCH HÀNG MUA HÀNG BETA",
    "buyer_operating_years": 5,
    "buyer_revenue_year_1": 60000000000,
    "buyer_revenue_year_2": 70000000000,
    "buyer_avg_revenue_2y": 65000000000,
    "contract_value": 20000000000,
    "loan_request_amount": 15000000000
  }
}
`

### Đoạn Prompt/Template 5
`	ext
{
  "assessment_id": "EB-BETA-CORP-2025-002",
  "company": {
    "name": "CÔNG TY CỔ PHẦN SẢN XUẤT VÀ XNK CÔNG NGHỆ BETA (MOCK AN DANH)",
    "tax_id": "0319888999",
    "industry": "Sản xuất Thiết bị Điện tử & Gia công Cơ khí Chính xác",
    "operating_years": 6,
    "legal_rep": "TRẦN VĂN BETA"
  },
  "reporting_period": "FY2025",
  "currency": "VND",
  "financials": {
    "BS_CURRENT_ASSETS": 185000000000,
    "BS_CURRENT_LIABILITIES": 92000000000,
    "BS_TRADE_RECEIVABLES": 45000000000,
    "BS_INVENTORY": 38000000000,
    "BS_TRADE_PAYABLES": 28000000000,
    "BS_SHORT_TERM_DEBT": 40000000000,
    "BS_TOTAL_LIABILITIES": 110000000000,
    "BS_EQUITY": 220000000000,
    "IS_REVENUE": 280000000000,
    "IS_GROSS_PROFIT": 56000000000,
    "IS_EBIT": 32000000000,
    "IS_INTEREST_EXPENSE": 4200000000,
    "IS_NET_PROFIT": 22000000000,
    "CF_OPERATING_CASH_FLOW": 26500000000,
    "CF_INVESTING_CASH_FLOW": -12000000000,
    "CF_FINANCING_CASH_FLOW": -8000000000,
    "PRINCIPAL_DUE": 10000000000
  },
  "dsp": {
    "revenue": 278000000000,
    "trade_receivables": 44500000000
  },
  "product_039": {
    "customer_operating_years": 6,
    "customer_equity": 220000000000,
    "buyer_name": "TẬP ĐOÀN CÔNG NGHỆ VÀ THIẾT BỊ ĐIỆN TỬ TOÀN CẦU (BUYER X)",
    "buyer_operating_years": 8,
    "buyer_avg_revenue_2y": 520000000000,
    "contract_value": 80000000000,
    "loan_request_amount": 60000000000
  }
}
`

### Đoạn Prompt/Template 6
`	ext
{
  "assessment_id": "RB-TIKTOK-001",
  "data_classification": "SYNTHETIC",
  "customer": {
    "customer_id": "KH01",
    "name": "PHẠM THANH BÌNH",
    "segment": "individual_business_owner",
    "business_channel": "TikTok Shop",
    "business_tenure_months": 24
  },
  "income": [
    {
      "type": "business",
      "monthly_amount": 2919000000,
      "verification_status": "verified",
      "eligible_percent": 0.08,
      "source": "synthetic tax / platform evidence"
    }
  ],
  "existing_debts": [
    {
      "type": "long_term_loan",
      "outstanding": 2700000000,
      "monthly_payment": 30000000
    },
    {
      "type": "short_term_loan",
      "outstanding": 39000000,
      "monthly_payment": 5000000
    }
  ],
  "credit_cards": [
    {
      "limit": 250000000,
      "balance": 108000000
    }
  ],
  "loan": {
    "product": "unsecured_working_capital_demo",
    "amount": 450000000,
    "annual_interest_rate": 0.225,
    "tenor_months": 48,
    "secured": false,
    "purpose": "Bổ sung vốn lưu động nhập khẩu trang y tế"
  },
  "documents": {
    "identity": true,
    "income_proof": true,
    "cic": true,
    "business_registration": true,
    "platform_evidence": true
  },
  "rules": {
    "max_dti": 0.55,
    "min_disposable_income": 5000000,
    "max_card_utilization": 0.8,
    "max_unverified_income_share": 0.35
  }
}
`

