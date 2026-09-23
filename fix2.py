import re

filepath = 'agents/eb_credit_agent.py'
with open(filepath, 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r'    @staticmethod\n    def _call_greennode_llm.*?def _credit_covenants'

new_methods = '''    @staticmethod
    def _call_greennode_llm(system_prompt: str, user_prompt: str) -> str:
        import requests
        import os
        api_key = os.environ.get("GREENNODE_API_KEY", "vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d")
        url = os.environ.get("GREENNODE_MAAS_URL", "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions")
        model = os.environ.get("GREENNODE_MODEL", "z-ai/glm-5.2-hackathon")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1500
        }
        try:
            r = requests.post(url, json=body, headers=headers, timeout=15)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return ""
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"LLM Error: {e}")
            return ""

    @staticmethod
    def _financial_deep_dive(metrics: Mapping[str, Decimal | None], ratios: Mapping[str, Decimal | None], flags: list[Mapping[str, Any]]) -> dict[str, Any]:
        """Generate qualitative deep-dive commentary using GreenNode LLM."""
        nwc = ratios.get("nwc")
        dscr = ratios.get("dscr")
        icr = ratios.get("icr")
        current_assets = metrics.get("current_assets")
        current_liabilities = metrics.get("current_liabilities")
        current_ratio = _ratio(current_assets, current_liabilities)
        equity = metrics.get("equity")
        de_ratio = _ratio(metrics.get("total_liabilities"), equity)
        net_profit = metrics.get("net_profit") or _first_value(metrics, ("IS_NET_PROFIT", "NET_PROFIT"))
        net_margin = _ratio(net_profit, metrics.get("revenue"))
        roe = _ratio(net_profit, equity)

        # Build context
        context_parts = [
            f"NWC: {_number(nwc)} VND, Current Ratio: {_number(current_ratio)}x",
            f"DSCR: {_number(dscr)}x, ICR: {_number(icr)}x",
            f"Net Margin: {_number(net_margin)}, ROE: {_number(roe)}",
            f"D/E Ratio: {_number(de_ratio)}x"
        ]
        context = " ".join(context_parts)

        sys_prompt = "Bạn là GĐ Tín dụng MSB Michael Nguyễn. Nguyên tắc: Tinh gọn thực chiến, chém thẳng vào tử huyệt dòng tiền. Hãy đọc các chỉ số sau và đưa ra nhận xét Rủi ro / Cơ hội siêu ngắn gọn (Mỗi mục 1 câu)."
        llm_reply = CreditAssessment._call_greennode_llm(sys_prompt, context)
        
        # Fallback if LLM fails
        if not llm_reply:
            llm_reply = "LLM Timeout. NWC > 0, thanh khoản cơ bản. DSCR/ICR cần xem xét."

        assessments = [
            {"area": "Thanh khoản & Vốn", "observation": f"NWC={_number(nwc)}", "assessment": "Đã phân tích bởi AI"},
            {"area": "Nhận định Giám đốc Tín dụng (AI)", "observation": "GreenNode Insight", "assessment": llm_reply}
        ]
        return {"assessments": assessments, "current_ratio": _number(current_ratio), "de_ratio": _number(de_ratio), "net_margin": _number(net_margin), "roe": _number(roe)}

    @staticmethod
    def _swot_analysis(metrics: Mapping[str, Decimal | None], ratios: Mapping[str, Decimal | None], flags: list[Mapping[str, Any]], product_039: Mapping[str, Any], supply_chain: Mapping[str, Any], anomaly_summary: Mapping[str, Any]) -> dict[str, Any]:
        """Generate 360-degree SWOT using GreenNode LLM."""
        nwc = ratios.get("nwc")
        dscr = ratios.get("dscr")
        cfo = metrics.get("operating_cash_flow")
        triggered_flags = [f.get("title") for f in flags if isinstance(f, Mapping) and f.get("triggered")]
        flag_str = ", ".join(triggered_flags) if triggered_flags else "Không"
        anomaly_count = anomaly_summary.get("triggered_count", 0)

        context_parts = [
            f"NWC: {_number(nwc)}, DSCR: {_number(dscr)}, CFO: {_number(cfo)}",
            f"Cảnh báo đỏ (Red Flags): {flag_str}",
            f"Bất thường sao kê: {anomaly_count} lỗi."
        ]
        context = " ".join(context_parts)

        sys_prompt = (
            "Bạn là GĐ Tín dụng MSB. Viết mô hình SWOT cho doanh nghiệp dựa trên dữ liệu. "
            "Trả về ĐÚNG định dạng JSON hợp lệ với 4 mảng: 'strengths', 'weaknesses', 'opportunities', 'threats'. "
            "Mỗi mảng chứa 1-2 câu ngắn gọn, tinh gọn thực chiến."
        )
        
        llm_reply = CreditAssessment._call_greennode_llm(sys_prompt, context)
        
        # Parse JSON
        import json
        swot_data = {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []}
        try:
            clean_reply = llm_reply.replace('`json', '').replace('`', '').strip()
            parsed = json.loads(clean_reply)
            for k in swot_data:
                if k in parsed and isinstance(parsed[k], list):
                    swot_data[k] = parsed[k]
        except Exception:
            swot_data["threats"].append("Lỗi Parse AI SWOT. Cảnh báo đỏ: " + flag_str)

        return swot_data

    @staticmethod
    def _credit_covenants'''

new_js = re.sub(pattern, new_methods, js, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_js)
