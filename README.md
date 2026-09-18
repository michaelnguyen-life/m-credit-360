# M-Credit 360 All-in-One Super Agent
**MSB AI Hackathon 2026 | Team 22 - Hattrick**  
**Leader:** Michael Nguyên (EB MSB)  
**Version:** 3.0 Unified (Merged EB + RB + MB02a + Statement Analyzer + Web Portal + Zalo Bot Gateway)

---

## 1. Giới Thiệu & Kiến Trúc Hợp Nhất (All-in-One Architecture)

Theo định hướng chuẩn hóa từ Ban Giám Khảo MSB và Ban Tổ Chức Hackathon (Tech Lead Phượng Nguyễn): **Mỗi đội thi triển khai đúng 01 Super Agent duy nhất** trên GreenNode AgentBase Runtime, tích hợp trọn vẹn cả 2 phân hệ **KHDN (Enterprise Banking - EB)** và **KHCN (Retail Banking - RB)**.

```text
                           +------------------------------------+
                           |        NGƯỜI DÙNG / GIÁM KHẢO      |
                           +-----------------+------------------+
                                             |
                     +-----------------------+-----------------------+
                     |                                               |
             [KÊNH DI ĐỘNG]                                  [KÊNH MÁY TÍNH / WEB]
       Zalo Bot (@bot.MaqROeGH)                       Web Portal Dashboard (GET /)
                     |                                               |
                     +-----------------------+-----------------------+
                                             |
                                             v
                      +---------------------------------------------+
                      |       M-CREDIT 360 ALL-IN-ONE SUPER AGENT   |
                      |          GreenNode AgentBase Runtime        |
                      |            Single /invocations API          |
                      +----------------------+----------------------+
                                             |
     +-------------------+-------------------+-------------------+-------------------+
     |                   |                   |                   |                   |
     v                   v                   v                   v                   v
+------------+     +------------+     +---------------+    +------------+    +---------------+
| Phân Hệ EB |     | Phân Hệ RB |     | MB02a Builder |    | Statement  |    | GreenNode     |
| KHDN >200T |     | KHCN/TikTok|     | Xuất Word 8 P |    | Rule 5D    |    | MaaS LLM      |
| NWC/DSCR   |     | DTI/Hạn mức|     | 21 Bảng biểu  |    | Anomaly    |    | Qwen3.6-Flash |
+------------+     +------------+     +---------------+    +------------+    +---------------+
```

---

## 2. Các Phân Hệ Chức Năng Cốt Lõi

### A. Phân Hệ Tín Dụng Doanh Nghiệp (EB Credit Assessment)
- **Động cơ phân tích BCTC deterministic**: Bóc tách chuẩn mã chỉ tiêu kế toán MSB (`BS001`, `BS002`, `IS001`, `IS003`, `CF...`).
- **Chỉ số an toàn tín dụng**:
  - Vốn lưu động ròng (*Net Working Capital - NWC* = TSNH - Nợ NH).
  - Nhu cầu vốn lưu động (*Working Capital Requirement - WCR*).
  - Hệ số khả năng trả nợ (*Debt Service Coverage Ratio - DSCR* = CFADS / Gốc lãi đến hạn, chuẩn MSB $\ge$ 1.0x).
  - Hệ số bù đắp lãi vay (*Interest Coverage Ratio - ICR* = EBIT / Lãi vay, chuẩn MSB $\ge$ 1.5x).
- **Hệ thống Cảnh báo Rủi ro (5 Red Flags)**: Mất cân đối vốn, CFO âm, Nợ ngắn hạn chiếm tỷ trọng cao, Sai lệch DSP/Digisale, Dòng tiền trả nợ suy yếu.
- **Tài trợ Chuỗi QĐ.EB.039**: Định cỡ hạn mức tài trợ phải thu (80%), thẩm định người mua $\ge$ 50 tỷ, cơ cấu bù trừ công nợ 2 chiều.
- **Cross-sell Alert**: Gói tài trợ SCF/LC (331), hạn mức FX tỷ giá ưu đãi, CASA Payroll, M-Smart Overnight Sweep.

### B. Phân Hệ Tín Dụng Cá Nhân & Hộ Kinh Doanh (RB Retail Credit)
- **Động cơ thẩm định KHCN**: Đánh giá DTI, thu nhập tích lũy khả dụng (*Disposable Income*), tỷ lệ sử dụng hạn mức thẻ tín dụng.
- **Tài trợ Hộ kinh doanh Kênh số / TikTok Shop**:
  - Doanh thu sàn TMĐT: Áp dụng tỷ lệ công nhận thực tế (8% doanh thu sàn).
  - Tính toán nghĩa vụ nợ khoản vay mới theo công thức niên kim (*Annuity Payment*).
  - Kiểm soát ngưỡng an toàn: DTI $\le$ 55%, Thu nhập tích lũy $\ge$ 5 triệu VND/tháng, Card Utilization $\le$ 80%.
  - Tự động kết xuất **Bản Tóm Tắt Tờ Trình Cá Nhân (Credit Memo)**.

### C. Động Cơ Khởi Tạo Tờ Trình Tín Dụng MB02a (Credit Memo Builder)
- Tự động điền dữ liệu tài chính vào biểu mẫu Tờ trình Tín dụng chuẩn hóa của MSB: **MB02a/QT.RR.037**.
- Cấu trúc hoàn chỉnh 8 Phần nghiệp vụ & 21 Bảng biểu:
  - Phần 1: Thông tin pháp lý & Khách hàng.
  - Phần 2: Nội dung đề xuất cấp tín dụng.
  - Phần 3: Thẩm định BCTC & Khả năng tài chính.
  - Phần 4: Thẩm định Chuỗi cung ứng.
  - Phần 5: Bóc tách bất thường Sao kê & Dòng tiền.
  - Phần 6: Đánh giá điều kiện sản phẩm QĐ.EB.039.
  - Phần 7: Phân tích ma trận SWOT.
  - Phần 8: Kết luận & Khung 4 chữ ký phê duyệt (B55).
- Xuất file `.docx` chuyên nghiệp chỉ sau 1 cú click!

### D. GreenNode MaaS AI Cloud (Ad-hoc Credit Analysis & Chatbot)
- Kết nối trực tiếp mô hình ngôn ngữ lớn `qwen/qwen3.6-flash` trên hạ tầng VNG Cloud MaaS.
- Đóng vai Chuyên gia Thẩm định Tín dụng MSB cấp cao:
  - Phân tích tức thì số liệu tài chính bất kỳ của KHDN/KHCN do người dùng nhập tự do.
  - Giải thích chi tiết các thuật ngữ tài chính, quy định MSB, cơ chế tài trợ chuỗi QĐ 039.

---

## 3. Song Trụ Tiếp Cận (Dual Channels)

### Kênh 1: Web Portal Dashboard (Desktop / Máy tính)
- Truy cập trực tiếp tại: `http://<domain-hoac-ip>:8080/`
- Giao diện **Glassmorphism** sang trọng, tông màu nhận diện thương hiệu MSB (Navy `#0A2540`, Orange `#FF6B00`, Emerald `#10B981`).
- Chuyển đổi tab linh hoạt:
  - Tab Doanh Nghiệp (EB): Nạp mẫu Alpha Group / Beta Corp, tính toán tự động, tải file Word MB02a.
  - Tab Cá Nhân (RB): Nạp mẫu TikTok Shop, tính DTI, xem Credit Memo cá nhân.
  - Tab Zalo Bot Mobile: Quét mã QR, xem hướng dẫn lệnh tác chiến.
  - AI Assistant Chat Drawer: Khung chat tư vấn tín dụng nổi tương tác thời gian thực.

### Kênh 2: Zalo Bot Gateway (Mobile / Di động)
- Tài khoản Bot: **Bot Agent EB 360** (`@bot.MaqROeGH`).
- Chạy 24/7 độc lập trên hạ tầng GreenNode, không phụ thuộc vào máy cá nhân.
- Các lệnh tác chiến nhanh:
  - `alpha`: Thẩm định BCTC Alpha Group (318 tỷ, NWC âm, DSCR 0.37x).
  - `beta`: Thẩm định BCTC Beta Corp (280 tỷ, DSCR 1.87x, Cross-sell QĐ 039).
  - `rb` hoặc `tiktok`: Thẩm định Tín dụng Hộ kinh doanh TikTok Shop.
  - `to trinh` hoặc `mb02a`: Kích hoạt xuất Tờ trình Tín dụng MB02a 8 phần.
  - `status`: Kiểm tra sức khỏe các Agent Runtime trên Cloud.
  - Nhập số liệu bất kỳ: AI giải phẫu tài chính ad-hoc trong 15 giây.
- **Cơ chế Giám sát & Phân quyền Chủ quyền (Leader Michael Nguyên)**:
  - Báo cáo ngầm tự động (Shadow Alert) về Zalo cá nhân Sếp Michael khi có người ngoài tương tác.
  - Lệnh thu hồi quyền truy cập tức thì: `/block [Chat_ID]` | Mở lại: `/unblock [Chat_ID]` | Xem danh sách: `/list`.

---

## 4. Danh Mục API Endpoints Chuẩn

| Method | Endpoint | Mô Tả Chức Năng | Phân Hệ |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Web Portal Glassmorphism Dashboard | Chung |
| `GET` | `/health` / `/ping` | Kiểm tra trạng thái runtime & capabilities | Chung |
| `POST` | `/invocations` | **Endpoint duy nhất chuẩn GreenNode AgentBase** (Tự phân luồng EB, RB, DOCX, Statement) | Hợp nhất |
| `POST` | `/assess` | Thẩm định BCTC Doanh nghiệp | EB |
| `POST` | `/rb/assess` | Thẩm định Tín dụng Cá nhân / Hộ kinh doanh | RB |
| `POST` | `/build-memo-docx` | Khởi tạo & Tải về Tờ trình Tín dụng MB02a (.docx) | EB |
| `POST` | `/api/chat` | Hỏi đáp Chuyên gia Tín dụng MSB (Qwen3.6-Flash) | AI MaaS |
| `GET` | `/api/sample/eb/alpha` | Lấy dữ liệu BCTC mẫu Alpha Group (318 tỷ) | Sample EB |
| `GET` | `/api/sample/eb/beta` | Lấy dữ liệu BCTC mẫu Beta Corp (280 tỷ) | Sample EB |
| `GET` | `/api/sample/rb/tiktok` | Lấy dữ liệu mẫu Hộ kinh doanh TikTok Shop | Sample RB |
| `POST` | `/zalo-webhook` | Webhook nhận tin nhắn từ Zalo Bot Platform | Zalo Gateway |

---

## 5. Chứng Minh Hiệu Quả (AEV 18,7 Tỷ VND)
Sản phẩm M-CREDIT 360 mang lại Giá trị Tác động Kinh tế Hàng năm (AEV) ước tính **18,7 Tỷ VND** dựa trên quy mô triển khai cho 300 RM Trọng tâm:
- Tiết kiệm 9 Tỷ VND chi phí vận hành (Tối giản 4 giờ làm việc/hồ sơ, thay thế 36 FTEs).
- Gia tăng 9,7 Tỷ VND doanh thu thuần (Tốc độ giải ngân nhanh giúp chốt deal tăng 10%, và kích hoạt hệ thống bán chéo tự động).
*(Xem chi tiết bảng tính tại file `CHUNG_MINH_HIEU_QUA_18_7_TY.md`)*

---

## 6. Hướng Dẫn Triển Khai (Deployment)

### Chạy Local / Kiểm thử nhanh
```powershell
python -m pip install -r requirements.txt
python server.py
```
Mở trình duyệt truy cập: `http://localhost:8080`

### Build Docker Container
```bash
docker build -t m-credit-360:latest .
docker run -p 8080:8080 -e ENABLE_ZALO_BOT=true m-credit-360:latest
```

---
*© 2026 Team 22 - Hattrick | MSB AI Hackathon 2026. Lãnh đạo dự án: Michael Nguyên.*
