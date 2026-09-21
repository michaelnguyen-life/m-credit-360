# 📦 GÓI HANDOFF CHO PHƯỢNG — M-INSIGHT 360
> **Team 22 Hattrick — MSB AI Hackathon 2026**
> **Leader:** Michael Nguyên (Giám đốc KHDN EB MSB)
> **Ngày đóng gói:** 21/09/2026

---

## 🔗 I. THÔNG TIN TRUY CẬP

| Hạng mục | Giá trị |
|---|---|
| **GitHub Repo** | `https://github.com/michaelnguyen-life/m-credit-360.git` |
| **Branch** | `main` |
| **GreenNode Endpoint (Live)** | `https://endpoint-920ea8b2-8ae4-4df2-99ea-ed0ea67de3c9.agentbase-runtime.aiplatform.vngcloud.vn` |
| **GreenNode API Key** | `vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d` |
| **GreenNode MaaS URL** | `https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions` |
| **Model backend** | `z-ai/glm-5.2-hackathon` |

---

## 🚀 II. CHẠY LOCAL TRÊN MÁY PHƯỢNG (3 BƯỚC)

### Bước 1: Clone repo
```bash
git clone https://github.com/michaelnguyen-life/m-credit-360.git
cd m-credit-360
```

### Bước 2: Cài dependencies
```bash
pip install -r requirements.txt
```

> **Yêu cầu:** Python 3.10+ (khuyến nghị 3.11)

File `requirements.txt` gồm:
```
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
python-docx>=1.1.0
requests>=2.31.0
pydantic>=2.6.0
python-multipart>=0.0.9
pypdf>=4.1.0
pandas>=2.2.0
openpyxl>=3.1.2
jinja2>=3.1.3
```

### Bước 3: Chạy server
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8080 --reload
```

Mở trình duyệt: **http://localhost:8080**

> [!TIP]
> Flag `--reload` giúp tự động restart khi sửa code, rất tiện để debug.

---

## 🐳 III. CHẠY BẰNG DOCKER (Giống GreenNode)

```bash
docker build -t m-insight-360 .
docker run -p 8080:8080 m-insight-360
```

Mở trình duyệt: **http://localhost:8080**

---

## 🏗️ IV. KIẾN TRÚC HỆ THỐNG (6 AGENT + 1 WEB)

```
M_CREDIT_360/
├── server.py                         ← FastAPI chính (All-in-One)
├── templates/
│   └── index.html                    ← Giao diện Web Portal (~2180 dòng)
├── static/
│   └── img/m_insight_logo.png        ← Logo M-Insight 360
├── agents/
│   ├── eb_credit_agent.py            ← Agent 1: Thẩm định KHDN SME (EB)
│   ├── retail_credit_agent.py        ← Agent 2: Thẩm định KHCN (RB)
│   ├── credit_memo_builder_agent.py  ← Agent 3: Xuất tờ trình MB02a (EB DOCX)
│   ├── rb_credit_memo_builder.py     ← Agent 4: Xuất tờ trình MB01A (RB DOCX)
│   ├── statement_analyzer_agent.py   ← Agent 5: Phân tích sao kê Rule 5D
│   └── policy_eligibility_agent.py   ← Agent 6: Đánh giá chính sách
├── data_test/                        ← Dữ liệu mẫu (Alpha Group, Beta Corp, RB TikTok Shop)
├── output_memos/                     ← Thư mục xuất DOCX tờ trình
├── Dockerfile                        ← Docker build cho GreenNode
├── requirements.txt                  ← Python dependencies
├── opencode.jsonc                    ← Cấu hình OpenCode (GLM 5.2 Hackathon)
└── .env.example                      ← Mẫu biến môi trường
```

---

## 🔌 V. DANH SÁCH API ENDPOINTS

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/` | Web Portal (giao diện chính) |
| `GET` | `/health` | Health check |
| `POST` | `/invocations` | **Unified endpoint** (GreenNode AgentBase) — Auto-route EB/RB |
| `POST` | `/assess` | Thẩm định KHDN SME (EB) |
| `POST` | `/rb/assess` | Thẩm định KHCN (RB) |
| `POST` | `/build-memo-docx` | Xuất tờ trình MB02a EB (.docx) |
| `POST` | `/rb/build-memo-docx` | Xuất tờ trình MB01A RB (.docx) |
| `POST` | `/rb/export-memo-docx` | Alias cho `/rb/build-memo-docx` |
| `POST` | `/api/upload` | Upload file BCTC (PDF/Excel/CSV) → bóc tách tự động |
| `POST` | `/api/chat` | Chat với AI qua GreenNode MaaS LLM |
| `POST` | `/policy/evaluate` | Đánh giá chính sách cho vay |
| `POST` | `/zalo-webhook` | Webhook Zalo Bot |

---

## 🤖 VI. PROMPT HỆ THỐNG AI (SYSTEM PROMPT - Chat Endpoint)

Đây là prompt được nhúng trong `/api/chat` (server.py dòng 358-366):

```
Bạn là M-CREDIT 360 AI - Chuyên gia Thẩm định Tín dụng Cấp cao của Ngân hàng MSB (Team 22 Hattrick).
Lãnh đạo: Michael Nguyên (Giám đốc KHDN EB MSB).
QUY TẮC:
1. Tuyệt đối KHÔNG viết tắt trơ trọi các chỉ số NWC, DSCR, ICR, WCR mà phải luôn ghi rõ TÊN TIẾNG VIỆT ĐẦY ĐỦ kèm công thức và ý nghĩa thẩm định MSB.
2. Phân tích bám sát khẩu vị rủi ro MSB: Vốn lưu động ròng NWC >= 0, Hệ số DSCR >= 1.0x, Hệ số ICR >= 1.5x, Rule 5D dòng tiền về MSB >= 80% Có 131.
3. Khi người dùng mới chỉ gửi thông tin tên công ty, MST, địa chỉ mà CHƯA có số liệu tài chính cụ thể, hãy xác nhận thông tin đã nhận và BẮT BUỘC dùng đúng câu: '* Lưu ý : Để xuất ngay BÁO CÁO SƠ BỘ, tôi cần bổ sung bộ dữ liệu tài chính thực tế của công ty trong 12–24 tháng gần nhất. Vui lòng cung cấp'.
4. Ngôn ngữ đĩnh đạc, chuyên nghiệp, sắc bén, đi thẳng vào bản chất tài chính.
```

---

## 🧪 VII. TEST NHANH CÁC CHỨC NĂNG

### 7.1 Test EB Assessment (Thẩm định KHDN)
```bash
curl -X POST http://localhost:8080/assess \
  -H "Content-Type: application/json" \
  -d '{
    "company": {"name": "CTY TEST PHUONG", "tax_id": "0101234567"},
    "financials": {
      "IS_REVENUE": 150000000000,
      "IS_NET_PROFIT": 8000000000,
      "BS_TRADE_RECEIVABLES": 20000000000,
      "BS_INVENTORY": 15000000000,
      "BS_TRADE_PAYABLES": 18000000000,
      "BS_SHORT_TERM_DEBT": 30000000000,
      "BS_TOTAL_LIABILITIES": 50000000000,
      "BS_EQUITY": 40000000000,
      "CF_OPERATING_CASH_FLOW": 12000000000,
      "BS_CURRENT_ASSETS": 60000000000,
      "BS_CURRENT_LIABILITIES": 45000000000,
      "IS_INTEREST_EXPENSE": 3000000000
    }
  }'
```

### 7.2 Test RB Assessment (Thẩm định KHCN)
```bash
curl -X POST http://localhost:8080/rb/assess \
  -H "Content-Type: application/json" \
  -d '{
    "segment": "RB",
    "applicant": {"name": "Nguyen Van Test", "cccd": "001099012345"},
    "income": [{"source": "Lương", "monthly": 25000000}],
    "existing_debts": [{"type": "Vay mua nhà", "monthly_payment": 5000000}]
  }'
```

### 7.3 Test Upload File BCTC
```bash
curl -X POST http://localhost:8080/api/upload \
  -F "file=@path/to/BCTC_2025.pdf"
```

### 7.4 Test Chat AI
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Phân tích chỉ số DSCR là gì?"}'
```

---

## ⚠️ VIII. CÁC LỖI ĐÃ BIẾT & CÁCH XỬ LÝ

### 8.1 Upload file PDF scan (ảnh) → trả về toàn 0
- **Nguyên nhân:** `pypdf` chỉ đọc được PDF text-based. PDF scan (ảnh chụp/quét) không có text layer → trích xuất = rỗng.
- **Fix tạm:** Hệ thống trả về giá trị 0 cho tất cả chỉ tiêu khi text < 50 ký tự và hiển thị `"FILE ẢNH/SCAN (KHÔNG CÓ TEXT)"`.
- **Fix triệt để:** Tích hợp OCR (Tesseract / EasyOCR / Google Vision API).

### 8.2 Tên công ty rút ra không chính xác
- **Nguyên nhân:** Regex trích xuất tên công ty từ nội dung PDF. Nếu BCTC không chứa dòng "Công ty TNHH/CP..." rõ ràng thì sẽ fallback dùng tên file.
- **Workaround:** Đặt tên file PDF theo format: `BCTC_2025_TEN_CONG_TY.pdf`

### 8.3 Nút bấm không phản hồi trên giao diện
- **Đã fix:** Các DOM ID không khớp đã được sửa (77/77 ID matched). Nếu vẫn gặp, kiểm tra Console (F12) để xem lỗi JavaScript.

### 8.4 OpenCode báo "Found multiple matches for oldString"
- **Nguyên nhân:** OpenCode dùng text matching để edit file HTML lớn → có nhiều đoạn text giống nhau.
- **Workaround:** Yêu cầu OpenCode KHÔNG edit code trực tiếp, chỉ chạy `git pull` + `docker build`.

---

## 🔧 IX. BIẾN MÔI TRƯỜNG (ENV)

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `GREENNODE_API_KEY` | *(hardcoded trong server.py)* | API Key GreenNode MaaS |
| `GREENNODE_MAAS_URL` | `https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions` | MaaS LLM endpoint |
| `GREENNODE_MODEL` | `z-ai/glm-5.2-hackathon` | Model cho chat AI |
| `ENABLE_ZALO_BOT` | `false` | Bật/tắt Zalo Bot gateway |

---

## 📋 X. OPENCODE — PROMPT DEPLOY LÊN GREENNODE

Nếu Phượng cần deploy lên GreenNode bằng OpenCode (GLM 5.2 Hackathon), copy prompt này:

```
NHIỆM VỤ: Deploy M-Insight 360 lên GreenNode AgentBase.

TUYỆT ĐỐI KHÔNG được edit bất kỳ file code nào (server.py, index.html, agents/*).
Chỉ thực hiện đúng 3 lệnh shell sau:

1. cd /path/to/m-credit-360 && git pull origin main
2. docker build -t m-insight-360 .
3. Deploy container lên GreenNode AgentBase endpoint hiện có.

Endpoint ID: 920ea8b2-8ae4-4df2-99ea-ed0ea67de3c9
Port: 8080
Health check: GET /health

Nếu build thành công, chạy: curl http://localhost:8080/health
để xác nhận status = "healthy".
```

---

## 🗂️ XI. CẤU TRÚC DỮ LIỆU MẪU

### 11.1 EB Payload Format (JSON)
```json
{
  "company": {
    "name": "CÔNG TY TNHH XYZ",
    "tax_id": "0312345678",
    "industry": "Xây dựng",
    "address": "TP. HCM"
  },
  "financials": {
    "IS_REVENUE": 150000000000,
    "IS_NET_PROFIT": 8000000000,
    "IS_INTEREST_EXPENSE": 3000000000,
    "BS_INVENTORY": 15000000000,
    "BS_TRADE_RECEIVABLES": 20000000000,
    "BS_TRADE_PAYABLES": 18000000000,
    "BS_SHORT_TERM_DEBT": 30000000000,
    "BS_TOTAL_LIABILITIES": 50000000000,
    "BS_EQUITY": 40000000000,
    "CF_OPERATING_CASH_FLOW": 12000000000,
    "BS_CURRENT_ASSETS": 60000000000,
    "BS_CURRENT_LIABILITIES": 45000000000
  }
}
```

### 11.2 RB Payload Format (JSON)
```json
{
  "segment": "RB",
  "applicant": {
    "name": "Nguyễn Văn A",
    "cccd": "001099012345",
    "phone": "0909123456",
    "address": "Quận 1, TP.HCM"
  },
  "income": [
    {"source": "Lương", "monthly": 25000000},
    {"source": "Kinh doanh TikTok Shop", "monthly": 15000000}
  ],
  "existing_debts": [
    {"type": "Vay mua nhà", "monthly_payment": 5000000, "bank": "VCB"}
  ],
  "credit_cards": [
    {"bank": "MSB", "limit": 50000000, "outstanding": 10000000}
  ],
  "loan_request": {
    "product": "Vay tiêu dùng tín chấp",
    "amount": 200000000,
    "tenor_months": 36,
    "purpose": "Bổ sung vốn kinh doanh online"
  }
}
```

---

## 📞 XII. LIÊN HỆ HỖ TRỢ

- **Michael Nguyên** (Team Lead): Zalo / Teams
- **Antigravity AI** (Tham Mưu Trưởng): Hỗ trợ debug code, kiến trúc, prompt engineering

---

> **🎯 Motto Team 22 Hattrick: "ĐÚNG - TINH - CHIẾN"**
