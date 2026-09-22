import io
import re

with io.open('agents/eb_credit_agent.py', 'r', encoding='utf-8') as f:
    agent = f.read()

# Add dynamic logic to ssess
dynamic_logic = '''
        # ---- DYNAMIC OSINT AND CROSS SELL INJECTION ----
        mst = payload.get("company", {}).get("tax_id", "")
        # Deterministic mock OSINT based on last digit of MST
        if mst and mst[-1] in ('8', '9'):
            profile["osint"] = {
                "tax_status": "Nợ 120Tr", "tax_class": "text-red-600",
                "bid_summary": "Đã trúng 3 gói", "bid_class": "text-blue-600",
                "bid_details": """
                    <div class="flex justify-between items-center"><span class="truncate pr-2">• Cung cấp VLXD</span><span class="font-mono font-bold text-slate-800">12,5 Tỷ</span></div>
                    <div class="flex justify-between items-center"><span class="truncate pr-2">• Thi công Trạm Y tế</span><span class="font-mono font-bold text-slate-800">8,2 Tỷ</span></div>
                    <div class="flex justify-between items-center"><span class="truncate pr-2">• Cải tạo Trường</span><span class="font-mono font-bold text-slate-800">4,1 Tỷ</span></div>
                """
            }
        else:
            profile["osint"] = {
                "tax_status": "Sạch (0đ)", "tax_class": "text-green-600",
                "bid_summary": "0 gói thầu", "bid_class": "text-slate-500",
                "bid_details": '<div class="text-slate-400 italic">Chưa ghi nhận lịch sử trúng thầu</div>'
            }

        # Dynamic cross sell
        deals = []
        ar = float(metrics.get("trade_receivables") or 0)
        ap = float(metrics.get("trade_payables") or 0)
        rev = float(metrics.get("revenue") or 0)
        
        if ar > 10e9:
            deals.append({
                "product": "Tài trợ Phải thu (QĐ 039)",
                "priority": "P1",
                "estimated_deal_size": ar * 0.8,
                "reasoning": "Doanh nghiệp có khoản phải thu lớn, cấp hạn mức tài trợ 80% giá trị phải thu giúp giải phóng vốn lưu động bị chiếm dụng."
            })
        if ap > 5e9:
            deals.append({
                "product": "Tài trợ SCF / L/C Nhập khẩu",
                "priority": "P2",
                "estimated_deal_size": ap * 0.5,
                "reasoning": "Dư nợ phải trả người bán cao, có thể bán chéo L/C nhập khẩu hoặc SCF thanh toán nhà cung cấp."
            })
        if rev > 50e9:
            deals.append({
                "product": "Bảo lãnh & Thanh toán QT",
                "priority": "P1",
                "estimated_deal_size": rev * 0.05,
                "reasoning": "Quy mô doanh thu lớn, cần giải pháp thanh toán quốc tế và bảo lãnh thực hiện hợp đồng."
            })
            
        profile["cross_sell_opportunities"] = deals
        # ------------------------------------------------
'''

# We need to insert this right before eturn profile
agent = agent.replace('        return profile', dynamic_logic + '\n        return profile')

with io.open('agents/eb_credit_agent.py', 'w', encoding='utf-8') as f:
    f.write(agent)
