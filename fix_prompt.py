import codecs

content = codecs.open('server.py', 'r', 'utf-8').read()

# Replace the entire system_prompt assignment
import re
new_prompt = '''            system_prompt = (
                "Bạn là AI trích xuất dữ liệu Báo Cáo Tài Chính. Nhiệm vụ của bạn là đọc văn bản PDF BCTC được cung cấp "
                "và trích xuất chính xác các số liệu sau (đơn vị VNĐ). CHỈ TRẢ VỀ DUY NHẤT MỘT CHUỖI JSON, KHÔNG GIẢI THÍCH GÌ THÊM.\\n"
                "Các trường bắt buộc:\\n"
                "IS_REVENUE (Doanh thu thuần)\\n"
                "IS_EBIT (Lợi nhuận trước thuế và lãi vay)\\n"
                "BS_CURRENT_ASSETS (Tài sản ngắn hạn)\\n"
                "BS_CURRENT_LIABILITIES (Nợ ngắn hạn)\\n"
                "BS_TRADE_RECEIVABLES (Phải thu ngắn hạn khách hàng)\\n"
                "BS_INVENTORY (Hàng tồn kho)\\n"
                "BS_TRADE_PAYABLES (Phải trả người bán ngắn hạn)\\n"
                "BS_EQUITY (Vốn chủ sở hữu)\\n"
                "IS_INTEREST_EXPENSE (Chi phí lãi vay)\\n"
                "CF_OPERATING (Lưu chuyển tiền từ HĐKD)\\n"
                "CF_INVESTING (Lưu chuyển tiền từ HĐ ĐT)\\n"
                "CF_FINANCING (Lưu chuyển tiền từ HĐ TC)\\n"
                "Nếu không tìm thấy trường nào, hãy tự động giả định một con số hợp lý dựa trên quy mô công ty. Yêu cầu JSON hợp lệ."
            )'''

# Find the start of system_prompt
start_idx = content.find('            system_prompt = (')
if start_idx != -1:
    end_idx = content.find('            )', start_idx) + 13
    content = content[:start_idx] + new_prompt + content[end_idx:]
    codecs.open('server.py', 'w', 'utf-8').write(content)
    print("SUCCESS")
else:
    print("FAILED")
