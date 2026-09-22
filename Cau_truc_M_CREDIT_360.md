# BẢN ĐỒ CẤU TRÚC GIAO DIỆN M-CREDIT 360

Tài liệu này giúp Sếp nắm rõ cấu trúc các khối (Blocks) trên trang chủ `index.html` để có thể tự thay đổi nội dung (Content) mà không làm vỡ giao diện (Layout) hay làm hỏng Logic (Javascript).

## I. NGUYÊN TẮC BẤT DI BẤT DỊCH TỪ ĐẶC VỤ
1. **Chỉ sửa nội dung TEXT (chữ tiếng Việt) nằm giữa các thẻ HTML** (ví dụ: `>Chữ cần sửa<`).
2. **TUYỆT ĐỐI KHÔNG sửa các `id="..."`, `class="..."`, hoặc `onclick="..."`** vì đây là các khớp nối thần kinh của Agent. Sửa chúng sẽ làm liệt tính năng.
3. **Tuyệt đối không dùng Notepad mặc định của Windows** để Save file HTML vì dễ sinh lỗi Font. Hãy dùng VSCode hoặc Notepad++.

## II. CẤU TRÚC 3 CỘT (GRID 4-5-3)
Giao diện Khách hàng Doanh nghiệp (EB) được chia thành 12 phần (Grid 12), chia làm 3 cột chính:

### 1. CỘT TRÁI (col-span-4): Form Nhập liệu
Bao gồm các nút điều khiển chính và Form nhập số liệu BCTC.
- **Các nút:** `+ Khách hàng mới`, `Upload hồ sơ`, `Alpha Group`, `Beta Corp`, `CHẠY THẨM ĐỊNH AI 360°`.
- **Vị trí sửa an toàn:** Tên các nút bấm (lưu ý không chạm vào `onclick="..."`).

### 2. CỘT GIỮA (col-span-5): Kết quả & Cảnh báo
Đây là khu vực hiển thị kết quả động từ Server. Các nội dung tĩnh CÓ THỂ sửa:
- Tiêu đề: `KẾT QUẢ THẨM ĐỊNH SƠ BỘ MSB`
- Tiêu đề 4 KPIs: `Vốn lưu động ròng`, `Hệ số trả nợ (DSCR)`, `Bù đắp lãi vay (ICR)`, `Tài trợ QĐ 039`.
- Khối `Trinh sát Dữ liệu (OSINT 360°)`: Đã chốt giữ lại 2 mục Nợ Thuế và Mua Sắm Công.
- Khối `Cảnh báo rủi ro (Red Flags)`

> [!WARNING] CƠ HỘI BÁN CHÉO LÀ DỮ LIỆU ĐỘNG
> Khối "Cơ hội Bán chéo (Cross-sell Alert)" không thể sửa bằng chữ tĩnh trong HTML, vì nó được sinh ra hoàn toàn TỰ ĐỘNG bằng code logic nằm trong file `eb_credit_agent.py`. Để sửa nội dung các deal (VD: Sửa "Tài trợ SCF" thành tên khác), Sếp phải mở file `eb_credit_agent.py` để sửa.

### 3. CỘT PHẢI (col-span-3): Danh mục Tài liệu
Khu vực chứa danh sách các file PDF, Excel đã tải lên.
- **Box 1:** Hồ sơ khách hàng (Hiển thị danh sách các file đã tải).
- **Ghi chú quan trọng:** Block `M-CREDIT AI Insight` (chứa dòng chữ DSCR 0.39x chốt cứng) **ĐÃ BỊ XÓA VĨNH VIỄN** ở bản hiện tại để đảm bảo tính logic cho KH mới. Khu vực này giờ hoàn toàn sạch sẽ.

## III. NÃO BỘ JAVASCRIPT
Nằm ở cuối cùng file `index.html`, bên trong thẻ `<script>`. Đây là não bộ điều khiển:
1. `runEBAssessment()`: Kích hoạt API thẩm định và điền dữ liệu động vào Cột Giữa.
2. `saveEBProfile()`: Lưu hồ sơ vào database.
3. `loadEBProfile(mst)`: Tự động gọi lại hồ sơ khi Sếp gõ MST.
4. `openNewCustomerModal()`: Xóa trắng Form cho Khách hàng mới.
