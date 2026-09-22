import io

with io.open('agents/eb_credit_agent.py', 'r', encoding='utf-8') as f:
    code = f.read()

injection = '''
        # ---- DYNAMIC OSINT & CROSS SELL ----
        mst = str(payload.get("company", {}).get("tax_id", "")).strip()
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
            deals = []
            rev = _number(metrics.get("revenue")) or 0
            if rev > 200000000000:
                deals.append({
                    "product": "Tài trợ Phải thu (SCF)",
                    "estimated_deal_size": rev * 0.15,
                    "priority": "P1",
                    "reasoning": '<div class="text-[10px] text-slate-500 bg-slate-50 p-2 mt-1 rounded border border-slate-100">Chu kỳ thu tiền (DSO) > 60 ngày. Có thể tài trợ ngay 80% hóa đơn.</div>'
                })
            deals.append({
                "product": "L/C Nhập khẩu & FX",
                "estimated_deal_size": 15000000000,
                "priority": "P2",
                "reasoning": '<div class="text-[10px] text-slate-500 bg-slate-50 p-2 mt-1 rounded border border-slate-100">Khoản phải trả tăng mạnh, nghi ngờ nhập khẩu nguyên liệu. Chốt tỷ giá Forward.</div>'
            })
            profile["cross_sell_opportunities"] = deals
        else:
            profile["osint"] = {
                "tax_status": "Sạch (0đ)", "tax_class": "text-green-600",
                "bid_summary": "0 gói thầu", "bid_class": "text-slate-500",
                "bid_details": '<div class="text-slate-400 italic">Chưa ghi nhận lịch sử trúng thầu</div>'
            }
            profile["cross_sell_opportunities"] = []
'''

target = 'profile["split_screen_demo"] = self._split_screen(payload, profile)'

if '# ---- DYNAMIC OSINT & CROSS SELL ----' not in code:
    code = code.replace(target, injection + '\n        ' + target)

with io.open('agents/eb_credit_agent.py', 'w', encoding='utf-8') as f:
    f.write(code)
