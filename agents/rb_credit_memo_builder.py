"""M-Insight 360 Retail Credit Proposal Builder (MB01A/QT.RR.038).

Fills official MSB MB01A credit application and assessment proposal from RB payload data.
Template: MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx
"""

from __future__ import annotations

import logging
import os
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Mapping

import docx

LOGGER = logging.getLogger("mcredit360.rb_memo")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TEMPLATE_PATH = os.path.join(
    os.path.dirname(BASE_DIR),
    "MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx"
)


def _money(val: Any) -> str:
    if val is None or val == "":
        return ""
    try:
        n = float(str(val).replace(",", "").replace(".", "").replace("VND", "").strip())
        return f"{int(n):,}".replace(",", ".") + " VND"
    except Exception:
        return str(val)


def _money_raw(val: Any) -> str:
    if val is None or val == "":
        return ""
    try:
        n = float(str(val).replace(",", "").replace(".", "").replace("VND", "").strip())
        return f"{int(n):,}".replace(",", ".")
    except Exception:
        return str(val)


class RetailCreditMemoBuilder:
    """Builds and outputs filled MSB MB01A DOCX."""

    def __init__(self, template_path: str | None = None, output_dir: str | None = None):
        self.template_path = template_path or DEFAULT_TEMPLATE_PATH
        if not os.path.exists(self.template_path):
            # Fallback search
            alt = os.path.join(BASE_DIR, "MB01A QT.RR.038 - Giay de nghi cap tin dung - lan 3.docx")
            if os.path.exists(alt):
                self.template_path = alt
        self.output_dir = output_dir or os.path.join(BASE_DIR, "output_memos")
        os.makedirs(self.output_dir, exist_ok=True)

    def build(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template MB01A not found at: {self.template_path}")

        doc = docx.Document(self.template_path)
        table = doc.tables[0]

        customer = payload.get("customer") or {}
        loan = payload.get("loan") or {}
        income_list = payload.get("income") or []
        debts = payload.get("existing_debts") or []
        ratios = payload.get("ratios") or {}

        # 1. Customer Details
        c_name = customer.get("name", "PHẠM THANH BÌNH")
        c_id = customer.get("customer_id", "KH01")
        c_cccd = customer.get("cccd") or customer.get("id_number") or "079090123456"
        c_phone = customer.get("phone") or "0908123456"
        c_email = customer.get("email") or "binh.pham@ecommerce-vietnam.vn"
        c_address = customer.get("address") or "124/8 Nguyễn Đình Chiểu, Phường Võ Thị Sáu, Quận 3, TP. Hồ Chí Minh"
        c_channel = customer.get("business_channel") or "TikTok Shop & Shopee Mall"

        # 2. Loan Details
        l_amt = loan.get("amount") or 450000000
        l_rate = loan.get("annual_interest_rate") or 0.225
        l_tenor = loan.get("tenor_months") or 48
        l_purpose = loan.get("purpose") or "Bổ sung vốn lưu động kinh doanh hàng tiêu dùng e-Commerce"

        # 3. Income & Financials
        inc_item = income_list[0] if income_list else {}
        gross_inc = inc_item.get("monthly_amount") or 2919000000
        eligible_pct = inc_item.get("eligible_percent") or 0.08
        eligible_inc = gross_inc * eligible_pct if gross_inc else 233520000

        total_debt_monthly = sum((d.get("monthly_payment") or 0) for d in debts) or 35000000
        total_debt_outstanding = sum((d.get("outstanding") or 0) for d in debts) or 2739000000
        living_cost = 20000000  # 20M standard living cost
        disposable_inc = eligible_inc - (total_debt_monthly + living_cost)

        # ==================== FILL TABLE CELLS ====================

        # Row 1: Hạn mức tín dụng đề nghị cấp
        table.rows[1].cells[0].text = f"Hạn mức tín dụng đề nghị cấp: {_money(l_amt)}"

        # Row 3: Họ tên khách hàng
        table.rows[3].cells[0].text = f"Họ tên: {c_name.upper()}"

        # Row 5: CCCD
        table.rows[5].cells[11].text = str(c_cccd)
        table.rows[5].cells[31].text = "Ngày cấp: 15/08/2021   Nơi cấp: Cục CSQLHC về TTXH"

        # Row 9: Địa chỉ thường trú
        table.rows[9].cells[5].text = c_address

        # Row 12: Điện thoại
        table.rows[12].cells[31].text = f"Điện thoại di động: {c_phone}"

        # Row 13: Email
        table.rows[13].cells[0].text = f"Email: {c_email}"

        # Row 21: Tên cơ sở kinh doanh
        table.rows[21].cells[0].text = f"Tên cơ sở kinh doanh*: HỘ KINH DOANH {c_name.upper()} ({c_channel})"

        # Row 22: Ngành nghề kinh doanh
        table.rows[22].cells[0].text = "Ngành nghề kinh doanh*: Bán lẻ hàng hóa qua mạng xã hội và sàn TMĐT (TikTok Shop, Shopee)"

        # Row 68: Thu nhập từ lương / chi phí
        table.rows[68].cells[17].text = "0"
        table.rows[68].cells[56].text = _money_raw(living_cost)

        # Row 69: Nghĩa vụ nợ khác
        table.rows[69].cells[56].text = _money_raw(total_debt_monthly)

        # Row 70: Thu nhập từ kinh doanh
        table.rows[70].cells[17].text = _money_raw(eligible_inc)

        # Row 72: TỔNG THU NHẬP (A) & TỔNG CHI PHÍ (B)
        total_costs = living_cost + total_debt_monthly
        table.rows[72].cells[17].text = _money_raw(eligible_inc)
        table.rows[72].cells[56].text = _money_raw(total_costs)

        # Row 73: Thu nhập tích lũy hàng tháng = (A) - (B)
        table.rows[73].cells[0].text = f"Thu nhập tích lũy hàng tháng* = (A) − (B) = {_money(disposable_inc)}"

        # Row 84 & 85: Chi tiết khoản vay
        table.rows[85].cells[0].text = "1"
        table.rows[85].cells[2].text = "Vay vốn lưu động KHCN"
        table.rows[85].cells[12].text = l_purpose
        table.rows[85].cells[32].text = _money_raw(l_amt)
        table.rows[85].cells[47].text = _money_raw(l_amt)
        table.rows[85].cells[63].text = f"{l_tenor} tháng"

        # Row 95, 96: Hạn mức khung
        table.rows[95].cells[4].text = _money(l_amt)
        table.rows[96].cells[4].text = f"{l_tenor} tháng (Lãi suất: {l_rate*100 if l_rate < 1 else l_rate}%/năm)"

        # Save to output file
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out_filename = f"TO_TRINH_KHCN_MB01A_{c_id}_{ts}.docx"
        out_path = os.path.join(self.output_dir, out_filename)
        doc.save(out_path)

        LOGGER.info("Built MB01A Retail Credit Proposal: %s", out_path)
        return {
            "status": "success",
            "memo_type": "MB01A/QT.RR.038",
            "file_name": out_filename,
            "file_path": out_path,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "customer_id": c_id,
            "customer_name": c_name,
            "approved_amount": l_amt
        }
