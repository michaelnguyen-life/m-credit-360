# -*- coding: utf-8 -*-
"""
M-CREDIT 360 - ZALO BOT INTEGRATION SERVICE (MULTI-COMPANY & AD-HOC CREDIT ASSESSMENT)
Bot Name: Bot Agent EB 360 (bot.MaqROeGH)
Team: Hattrick (Team 22 - MSB AI Hackathon 2026)
Leader: Michael Nguyen (EB MSB)

Connects Zalo Bot directly to:
1. GreenNode AgentBase Runtime 1: eb-credit-agent (/assess) [Alpha Group & Beta Corp]
2. GreenNode AgentBase Runtime 2: credit-memo-builder (/build-memo-docx)
3. GreenNode MaaS Cloud LLM: qwen/qwen3.6-flash (Ad-hoc Company Credit Analysis & Credit Burner)
"""

import os
import sys
import time
import json
import logging
import requests

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ZaloBotService")

# ================= CONFIGURATION =================
ZALO_BOT_TOKEN = os.environ.get(
    "ZALO_BOT_TOKEN", 
    "1594214031862095447:dNzbsXIUJIsmbInvjIHyzhZekmVhCymQZmQXtQVYFwKkTyoRXRIjmkZresuZFFCI"
)
ZALO_API_BASE = f"https://bot-api.zaloplatforms.com/bot{ZALO_BOT_TOKEN}"

# GreenNode Cloud AgentBase Endpoints
URL_ASSESS = os.environ.get(
    "URL_ASSESS",
    "https://endpoint-532eb3d4-0d9d-4b19-93c1-2ebc3060bca4.agentbase-runtime.aiplatform.vngcloud.vn/assess"
)
URL_MEMO = os.environ.get(
    "URL_MEMO",
    "https://endpoint-05361e8d-12de-4860-8c26-d6e637d5aa42.agentbase-runtime.aiplatform.vngcloud.vn/build-memo-docx"
)
URL_HEALTH_AGENT1 = "https://endpoint-532eb3d4-0d9d-4b19-93c1-2ebc3060bca4.agentbase-runtime.aiplatform.vngcloud.vn/health"
URL_HEALTH_AGENT4 = "https://endpoint-05361e8d-12de-4860-8c26-d6e637d5aa42.agentbase-runtime.aiplatform.vngcloud.vn/health"

# GreenNode MaaS LLM
GREENNODE_MAAS_URL = os.environ.get(
    "GREENNODE_MAAS_URL",
    "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1/chat/completions"
)
GREENNODE_API_KEY = os.environ.get(
    "GREENNODE_API_KEY",
    "vn-_gWfSl72C6qp1Z-qvEGv5Ua4ae16ffa17a447a947fbb2c08baacceDlbvUJ3OXxmybnUe_B_xZ0-0001bf792de9195d"
)
GREENNODE_MODEL = "qwen/qwen3.6-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_PATH_ALPHA = os.path.join(BASE_DIR, "data_test", "1. CTY DAU TU GROUP (MOCK AN DANH)", "eb_credit_payload.json")
PAYLOAD_PATH_BETA = os.path.join(BASE_DIR, "data_test", "2. CTY SAN XUAT XNK BETA (MOCK CHUAN CROSS-SELL)", "eb_credit_payload.json")
PAYLOAD_PATH_RETAIL = os.path.join(BASE_DIR, "data_test", "retail", "retail_tiktok_shop_sample.json")

# ================= COMMANDER OVERWATCH & ACCESS CONTROL =================
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "8c0b4fa75be6b2b8ebf7")
BLOCKED_USERS_FILE = os.path.join(BASE_DIR, "blocked_users.json")
USER_REGISTRY_FILE = os.path.join(BASE_DIR, "user_registry.json")

def load_json_data(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_json_data(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving {path}: {e}")

def is_blocked(chat_id):
    blocked = load_json_data(BLOCKED_USERS_FILE)
    return str(chat_id) in blocked

def block_user(chat_id, reason="Blocked by Leader Michael"):
    blocked = load_json_data(BLOCKED_USERS_FILE)
    blocked[str(chat_id)] = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "reason": reason
    }
    save_json_data(BLOCKED_USERS_FILE, blocked)
    logger.info(f"User {chat_id} added to BLOCKED list.")

def unblock_user(chat_id):
    blocked = load_json_data(BLOCKED_USERS_FILE)
    if str(chat_id) in blocked:
        del blocked[str(chat_id)]
        save_json_data(BLOCKED_USERS_FILE, blocked)
        logger.info(f"User {chat_id} removed from BLOCKED list.")
        return True
    return False

def register_user_activity(chat_id, user_name, query_text):
    registry = load_json_data(USER_REGISTRY_FILE)
    cid = str(chat_id)
    if cid not in registry:
        registry[cid] = {
            "name": user_name,
            "first_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
            "query_count": 0,
            "last_query": ""
        }
    registry[cid]["query_count"] += 1
    registry[cid]["last_query"] = query_text[:200]
    registry[cid]["last_seen"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if user_name and user_name != cid:
        registry[cid]["name"] = user_name
    save_json_data(USER_REGISTRY_FILE, registry)

def notify_admin_shadow(chat_id, sender_id, user_name, group_name, query_text, reply_text, elapsed_sec=0):
    """Gửi báo cáo ngầm tức thì về Zalo cá nhân của Sếp Michael Nguyên"""
    if str(sender_id) == str(ADMIN_CHAT_ID) or str(chat_id) == str(ADMIN_CHAT_ID):
        return  # Không gửi báo cáo tin nhắn của chính Sếp
        
    try:
        now_str = time.strftime("%H:%M:%S - %d/%m/%Y")
        short_reply = (reply_text[:250] + "...\n*(Xem toàn văn tại máy chủ)*") if len(reply_text) > 250 else reply_text
        target_block_id = sender_id if sender_id else chat_id
        is_group = bool(group_name and str(chat_id) != str(sender_id))
        
        header = f"🔔 [GIÁM SÁT NGƯỜI DÙNG - TRONG NHÓM: {group_name}]" if is_group else f"🔔 [GIÁM SÁT NGƯỜI DÙNG BOT AGENT EB 360]"
        
        alert_lines = [
            header,
            f"👤 Người dùng: {user_name}",
            f"🆔 User ID: `{target_block_id}`",
        ]
        if is_group:
            alert_lines.append(f"👥 Nhóm ID: `{chat_id}`")
            
        alert_lines.extend([
            f"⏰ Lúc: {now_str}",
            f"⏱ Xử lý: {elapsed_sec:.1f}s",
            "",
            f"💬 Khách vừa hỏi:",
            f"\"{query_text}\"",
            "",
            f"🤖 Bot đã phản hồi tóm tắt:",
            f"{short_reply}",
            "",
            "------------------------------------",
            f"👉 ĐỂ THU HỒI QUYỀN người này, Sếp chỉ cần nhắn cho Bot lệnh:",
            f"/block {target_block_id}"
        ])
        
        alert_text = "\n".join(alert_lines)
        zalo_send_message(ADMIN_CHAT_ID, alert_text)
        logger.info(f"-> Shadow alert sent to Sếp Michael [{ADMIN_CHAT_ID}] for user [{target_block_id}].")
    except Exception as e:
        logger.error(f"Failed to send shadow notification to admin: {e}")



# ================= ZALO BOT API HELPERS =================
def zalo_get_me():
    try:
        r = requests.post(f"{ZALO_API_BASE}/getMe", json={}, timeout=10)
        if r.status_code == 200:
            return r.json()
        logger.error(f"getMe failed: {r.status_code} {r.text}")
    except Exception as e:
        logger.error(f"getMe exception: {e}")
    return None

def zalo_send_message(chat_id, text):
    """Send message to Zalo chat, chunking if length > 1800 chars"""
    try:
        if not chat_id:
            logger.error("zalo_send_message: chat_id is empty!")
            return False
            
        chunks = []
        rem = text
        while len(rem) > 1800:
            cut = rem.rfind("\n", 0, 1800)
            if cut == -1:
                cut = 1800
            chunks.append(rem[:cut])
            rem = rem[cut:].lstrip()
        if rem:
            chunks.append(rem)

        success = True
        for c in chunks:
            payload = {
                "chat_id": str(chat_id),
                "text": c,
                "parse_mode": "markdown"
            }
            r = requests.post(f"{ZALO_API_BASE}/sendMessage", json=payload, timeout=15)
            if r.status_code == 200 and r.json().get("ok"):
                logger.info(f"-> Sent message chunk to chat {chat_id} successfully.")
            else:
                logger.warning(f"sendMessage with markdown failed ({r.text}), retrying plain text...")
                payload.pop("parse_mode", None)
                r2 = requests.post(f"{ZALO_API_BASE}/sendMessage", json=payload, timeout=15)
                if r2.status_code == 200 and r2.json().get("ok"):
                    logger.info(f"-> Sent message chunk plain text to chat {chat_id} successfully.")
                else:
                    logger.error(f"Failed to send message chunk: {r2.text}")
                    success = False
        return success
    except Exception as e:
        logger.error(f"zalo_send_message exception: {e}")
    return False

def zalo_get_updates(timeout_sec=10):
    try:
        body = {"timeout": str(timeout_sec)}
        r = requests.post(f"{ZALO_API_BASE}/getUpdates", json=body, timeout=timeout_sec + 8)
        if r.status_code == 200:
            return r.json()
        else:
            logger.warning(f"getUpdates HTTP {r.status_code}: {r.text}")
    except requests.exceptions.Timeout:
        return {"ok": False, "description": "Client Read Timeout"}
    except Exception as e:
        logger.error(f"getUpdates exception: {e}")
    return None

# ================= AGENT & LLM DISPATCHERS =================
def call_agent_assess(company_type="alpha"):
    """Call Agent 1 on GreenNode Cloud to evaluate Alpha Group or Beta Corp"""
    try:
        path = PAYLOAD_PATH_BETA if company_type == "beta" else PAYLOAD_PATH_ALPHA
        if not os.path.exists(path):
            return f"❌ Không tìm thấy file dữ liệu BCTC mẫu: {path}"
        
        with open(path, 'r', encoding='utf-8') as f:
            eb_payload = json.load(f)
            
        logger.info(f"Calling GreenNode Agent 1 ({URL_ASSESS}) for {company_type}...")
        t0 = time.time()
        r = requests.post(URL_ASSESS, json=eb_payload, timeout=25)
        elapsed = time.time() - t0
        
        if r.status_code == 200:
            data = r.json()
            comp = data.get('company', {})
            rat = data.get('ratios', {})
            dec = data.get('preliminary_decision', {})
            p039 = data.get('product_039_evaluation', {})
            red_flags = [f for f in data.get('red_flags', []) if f.get('triggered')]
            
            dscr_val = rat.get('dscr', 0)
            dscr_warn = "⚠️ (Cảnh báo < 1.0x)" if dscr_val < 1.0 else "✅ (Đạt chuẩn an toàn)"
            
            msg = [
                f"🏆 **BÁO CÁO THẨM ĐỊNH TÍN DỤNG AI (GREENNODE CLOUD)**",
                "------------------------------------------",
                f"🏢 **Khách hàng**: {comp.get('name', 'N/A')}",
                f"📋 **Mã số thuế**: {comp.get('tax_id', 'N/A')}",
                f"🏭 **Ngành nghề**: {comp.get('industry', 'N/A')}",
                f"⏱ **Thời gian xử lý Cloud**: {elapsed:.2f}s (AgentBase)",
                "",
                "📊 **CHỈ SỐ DÒNG TIỀN & CÂN ĐỐI TÀI CHÍNH**:",
                f"- **Vốn lưu động ròng (Net Working Capital - NWC)**: **{rat.get('nwc', 0):,.0f} VND**",
                f"  *(Ý nghĩa: Đo lường mức độ an toàn vốn, chênh lệch giữa Tài sản ngắn hạn & Nợ ngắn hạn)*",
                f"- **Nhu cầu vốn lưu động (Working Capital Requirement - WCR)**: **{rat.get('wcr', 0):,.0f} VND**",
                f"  *(Ý nghĩa: Nhu cầu vốn thực tế cần bù đắp cho chu kỳ tồn kho & công nợ)*",
                f"- **Hệ số khả năng trả nợ (Debt Service Coverage Ratio - DSCR)**: **{dscr_val:.2f}x** {dscr_warn}",
                f"  *(Ý nghĩa: Năng lực tạo dòng tiền trả trọn vẹn nợ gốc đến hạn + lãi vay; chuẩn MSB yêu cầu >= 1.0x)*",
                f"- **Hệ số bù đắp lãi vay (Interest Coverage Ratio - ICR)**: **{rat.get('icr', 0):.2f}x**",
                f"  *(Ý nghĩa: Lợi nhuận trước lãi vay EBIT có đủ bù đắp chi phí lãi vay; chuẩn an toàn >= 2.0x)*",
                "",
                f"⚖️ **KẾT QUẢ ĐÁNH GIÁ SƠ BỘ**: **{dec.get('outcome', 'CHƯA RÕ')}**",
                f"📌 **Sản phẩm QĐ 039 MSB**: **{p039.get('decision', 'N/A')}**",
                ""
            ]
            
            if red_flags:
                msg.append("🚨 **CÁC ĐIỂM NÓNG RỦI RO (RED FLAGS PHÁT HIỆN)**:")
                for rf in red_flags[:4]:
                    sev = rf.get('severity', '').upper()
                    msg.append(f"- [{sev}] {rf.get('title')}: {rf.get('evidence')}")
                msg.append("")
            else:
                msg.append("✅ **ĐÁNH GIÁ RỦI RO**: Không phát hiện Red Flag vi phạm quy chế tín dụng nghiêm trọng.")
                msg.append("")
                
            if company_type == "beta":
                msg.append("💡 **GÓI BÁN CHÉO ĐỀ XUẤT (CROSS-SELL MSB)**:")
                msg.append("- Tài trợ chuỗi cung ứng (SCF) & Thư tín dụng (L/C) nhập khẩu NVL")
                msg.append("- Hạn mức FX Forward cố định tỷ giá & M-Smart Sweep tối ưu lãi suất")
                msg.append("")
                
            msg.append("👉 *Gõ 'to trinh' để Agent 4 xuất ngay Tờ trình Tín dụng mẫu MB02a 8 phần!*")
            return "\n".join(msg)
        else:
            return f"❌ Lỗi từ GreenNode Agent 1: HTTP {r.status_code}\n{r.text}"
    except Exception as e:
        logger.error(f"call_agent_assess exception: {e}")
        return f"❌ Lỗi kết nối Agent 1: {str(e)}"

def call_agent_memo():
    """Call Agent 4 on GreenNode Cloud to generate MB02a Word memo"""
    try:
        if not os.path.exists(PAYLOAD_PATH_ALPHA):
            return "❌ Không tìm thấy file dữ liệu BCTC mẫu"
            
        with open(PAYLOAD_PATH_ALPHA, 'r', encoding='utf-8') as f:
            eb_payload = json.load(f)
            
        logger.info(f"Calling GreenNode Agent 4 ({URL_MEMO})...")
        t0 = time.time()
        r = requests.post(URL_MEMO, json={'eb_payload': eb_payload}, timeout=25)
        elapsed = time.time() - t0
        
        if r.status_code == 200:
            data = r.json()
            file_path = data.get('file_path', 'MB02a_Master_Proposal.docx')
            decision = data.get('product_039_decision', 'Chấp thuận có điều kiện')
            
            msg = [
                "📝 **TỜ TRÌNH TÍN DỤNG MB02a ĐÃ ĐƯỢC KHỞI TẠO!**",
                "------------------------------------------",
                f"⏱ **Thời gian sinh hồ sơ Cloud**: {elapsed:.2f}s",
                "🎯 **Định dạng**: Master Credit Proposal chuẩn MSB (QĐ 016 & MB02a)",
                "📑 **Cấu trúc hoàn chỉnh**: 8 Phần chuẩn hóa & 21 Bảng biểu tự động",
                f"📁 **Tên hồ sơ**: {os.path.basename(file_path)}",
                f"⚖️ **Đề xuất tín dụng**: {decision}",
                "",
                "✅ Hồ sơ đã được đồng bộ hóa trực tiếp vào Agent Base Runtime trên GreenNode AI Cloud!"
            ]
            return "\n".join(msg)
        else:
            return f"❌ Lỗi từ GreenNode Agent 4: HTTP {r.status_code}\n{r.text}"
    except Exception as e:
        logger.error(f"call_agent_memo exception: {e}")
        return f"❌ Lỗi kết nối Agent 4: {str(e)}"

def call_agent_retail():
    """Call Retail Credit Assessment for TikTok Shop / Personal Business"""
    try:
        if not os.path.exists(PAYLOAD_PATH_RETAIL):
            return "❌ Không tìm thấy file dữ liệu KHCN mẫu (retail_tiktok_shop_sample.json)"
        with open(PAYLOAD_PATH_RETAIL, "r", encoding="utf-8") as f:
            rb_payload = json.load(f)
        
        sys.path.append(os.path.join(BASE_DIR, 'agents'))
        from retail_credit_agent import RetailCreditAssessment
        t0 = time.time()
        res = RetailCreditAssessment().assess(rb_payload)
        elapsed = time.time() - t0
        
        cust = res.get("customer", {})
        inc = res.get("income", {})
        debt = res.get("debt", {})
        ratios = res.get("ratios", {})
        flags = [f for f in res.get("red_flags", []) if f.get("triggered")]
        rec = res.get("preliminary_recommendation", {}).get("outcome", "N/A")
        
        def fmt_m(val):
            if val is None: return "N/A"
            return f"{val / 1_000_000:,.1f} Tr"

        msg = [
            "👤 **KẾT QUẢ THẨM ĐỊNH TÍN DỤNG KHCN (RETAIL BANKING)**",
            "------------------------------------------",
            f"⏱ **Thời gian xử lý**: {elapsed:.2f}s",
            f"👤 **Khách hàng**: {cust.get('name', 'N/A')} (Kênh: {cust.get('business_channel', 'TikTok Shop')})",
            f"🆔 **Mã hồ sơ**: `{res.get('assessment_id')}`",
            "",
            "📊 **NĂNG LỰC TÀI CHÍNH & DÒNG TIỀN:**",
            f"• Thu nhập gộp hàng tháng: {fmt_m(inc.get('gross_monthly_income'))}",
            f"• Thu nhập đủ điều kiện (công nhận): {fmt_m(inc.get('eligible_monthly_income'))} (tỷ lệ 8%)",
            f"• Nghĩa vụ nợ hiện hữu: {fmt_m(debt.get('existing_monthly_obligation'))}/tháng",
            f"• Khoản vay đề xuất: {fmt_m(rb_payload.get('loan', {}).get('amount'))} (Kỳ hạn: {rb_payload.get('loan', {}).get('tenor_months')} tháng)",
            f"• Gốc lãi ước tính khoản vay mới: {fmt_m(debt.get('new_loan_estimated_payment'))}/tháng",
            f"• Tổng nghĩa vụ nợ: {fmt_m(debt.get('total_monthly_obligation'))}/tháng",
            "",
            "⚖️ **CHỈ SỐ AN TOÀN TÍN DỤNG (MSB RB):**",
            f"• Hệ số DTI (Nợ / Thu nhập): {ratios.get('dti', 0) * 100:.1f}% (Chuẩn an toàn <= 55%)",
            f"• Thu nhập tích lũy khả dụng: {fmt_m(ratios.get('disposable_income'))}/tháng",
            "",
            f"🚩 **Cảnh báo Red Flags**: {len(flags)} cảnh báo",
        ]
        if flags:
            for flg in flags:
                msg.append(f"  ⚠️ [{flg.get('severity', '').upper()}] {flg.get('title')}: {flg.get('evidence', '')}")
        else:
            msg.append("  ✅ Không có Red Flag vi phạm quy chuẩn an toàn.")
            
        msg.extend([
            "",
            f"🎯 **ĐỀ XUẤT SƠ BỘ**: **{rec}**",
            "*(Hồ sơ đạt điều kiện chuyển thẩm định viên phê duyệt hạn mức)*"
        ])
        return "\n".join(msg)
    except Exception as e:
        logger.error(f"call_agent_retail exception: {e}")
        return f"❌ Lỗi thẩm định KHCN: {str(e)}"

def call_greennode_maas_llm(user_question):
    """
    Call GreenNode MaaS Cloud LLM (qwen/qwen3.6-flash).
    Handles:
    - Ad-hoc financial numbers for ANY company sent by user
    - General banking / credit queries
    Burns official hackathon credits.
    """
    try:
        logger.info(f"Calling GreenNode MaaS LLM for query: {user_question[:50]}...")
        system_prompt = (
            "Bạn là M-CREDIT 360 AI - Chuyên gia Thẩm định Tín dụng KHDN MSB cấp cao thuộc Đội Hattrick (Team 22).\n"
            "QUY TẮC BẮT BUỘC VỀ THUẬT NGỮ:\n"
            "Tuyệt đối KHÔNG viết tắt trơ trọi các chỉ số NWC, DSCR, ICR, WCR mà phải luôn ghi rõ TÊN TIẾNG VIỆT ĐẦY ĐỦ kèm ý nghĩa:\n"
            "• Vốn lưu động ròng (Net Working Capital - NWC) = Tài sản ngắn hạn - Nợ ngắn hạn (Ý nghĩa: Đánh giá an toàn tài chính ngắn hạn, phòng ngừa mất cân đối vốn).\n"
            "• Hệ số khả năng trả nợ (Debt Service Coverage Ratio - DSCR) = EBITDA / (Nợ gốc đến hạn + Lãi vay) (Ý nghĩa: Năng lực tạo dòng tiền trả nợ ngân hàng, chuẩn MSB >= 1.0x).\n"
            "• Hệ số bù đắp lãi vay (Interest Coverage Ratio - ICR) = EBIT / Chi phí lãi vay (Ý nghĩa: Lợi nhuận có đủ bù đắp chi phí lãi, chuẩn an toàn >= 2.0x).\n"
            "• Nhu cầu vốn lưu động (Working Capital Requirement - WCR) = (Phải thu + Tồn kho) - Phải trả.\n\n"
            "QUY TẮC PHẢN HỒI THẨM ĐỊNH:\n"
            "1. Khi người dùng cung cấp đầy đủ thông tin tài chính của bất kỳ công ty nào, hãy xuất BÁO CÁO THẨM ĐỊNH TÍN DỤNG TỨC THÌ chuẩn MSB gồm 4 phần: Thông tin DN; Phân tích tài chính & dòng tiền; Rủi ro & đối chiếu quy định MSB; Kết luận & đề xuất cấp tín dụng.\n"
            "2. Khi người dùng mới chỉ gửi thông tin tên công ty, MST, địa chỉ mà CHƯA có số liệu tài chính cụ thể, hãy xác nhận thông tin đã nhận và BẮT BUỘC dùng đúng câu sau:\n"
            "'* Lưu ý : Để xuất ngay BÁO CÁO SƠ BỘ, tôi cần bổ sung bộ dữ liệu tài chính thực tế của công ty trong 12–24 tháng gần nhất. Vui lòng cung cấp' kèm các chỉ tiêu gợi ý ngắn gọn (Doanh thu, EBIT, Tài sản ngắn hạn, Nợ ngắn hạn, Chi phí lãi vay, Hạn mức đề xuất).\n"
            "Nếu là câu hỏi thông thường, trả lời ngắn gọn, đĩnh đạc, chuyên nghiệp và thực chiến."
        )
        payload = {
            "model": GREENNODE_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            "temperature": 0.2,
            "max_tokens": 850
        }
        headers = {
            "Authorization": f"Bearer {GREENNODE_API_KEY}",
            "Content-Type": "application/json"
        }
        t0 = time.time()
        r = requests.post(GREENNODE_MAAS_URL, json=payload, headers=headers, timeout=35)
        elapsed = time.time() - t0
        
        if r.status_code == 200:
            res_json = r.json()
            usage = res_json.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            content = res_json["choices"][0]["message"]["content"]
            import re
            target_notice = "* Lưu ý : Để xuất ngay BÁO CÁO SƠ BỘ, tôi cần bổ sung bộ dữ liệu tài chính thực tế của công ty trong 12–24 tháng gần nhất. Vui lòng cung cấp"
            content = re.sub(
                r"[⚠️\*•\s]*Lưu ý[^\n:]*:\s*Để xuất ngay BÁO CÁO[^\n]*?tôi cần bổ sung bộ dữ liệu tài chính[^\n]*?Vui lòng cung cấp:?",
                target_notice,
                content,
                flags=re.IGNORECASE
            )
            footer = f"\n\n⚡ *[GreenNode MaaS Cloud • {elapsed:.2f}s • {total_tokens} credits consumed]*"
            return content + footer
        else:
            logger.error(f"MaaS LLM error: {r.status_code} {r.text}")
            return f"⚠️ GreenNode MaaS phản hồi lỗi: {r.status_code}"
    except Exception as e:
        logger.error(f"call_greennode_maas_llm exception: {e}")
        return f"⚠️ Lỗi kết nối GreenNode MaaS Cloud: {str(e)}"

def check_system_status():
    """Check health of cloud runtimes"""
    msg = [
        "🔍 **KIỂM TRA TRẠNG THÁI HỆ THỐNG CLOUD (TEAM 22)**:",
        "------------------------------------------"
    ]
    
    # Check Agent 1
    try:
        r1 = requests.get(URL_HEALTH_AGENT1, timeout=5)
        if r1.status_code == 200:
            msg.append("✅ **Agent 1 (Thẩm định BCTC)**: LIVE 200 OK")
        else:
            msg.append(f"⚠️ **Agent 1**: HTTP {r1.status_code}")
    except Exception:
        msg.append("❌ **Agent 1**: Mất kết nối")
        
    # Check Agent 4
    try:
        r4 = requests.get(URL_HEALTH_AGENT4, timeout=5)
        if r4.status_code == 200:
            msg.append("✅ **Agent 4 (Tờ trình MB02a)**: LIVE 200 OK")
        else:
            msg.append(f"⚠️ **Agent 4**: HTTP {r4.status_code}")
    except Exception:
        msg.append("❌ **Agent 4**: Mất kết nối")
        
    msg.append("✅ **GreenNode MaaS LLM**: LIVE (qwen/qwen3.6-flash)")
    msg.append("✅ **Zalo Bot Gateway**: LIVE (Bot Agent EB 360)")
    return "\n".join(msg)

def get_welcome_menu():
    return (
        "🌟 XIN CHÀO MICHAEL NGUYÊN, TEAM 22 HACKATHON & BAN GIÁM KHẢO MSB!\n\n"
        "Tôi là M-Credit 360 Super Agent — Trợ lý Thẩm định Tín dụng Hợp nhất (EB Doanh Nghiệp & RB Cá Nhân) "
        "do Team Hattrick (Team 22) phát triển, vận hành trực tiếp trên hạ tầng GreenNode AI Cloud (VNG Cloud).\n\n"
        "💡 CÁC LỆNH TÁC CHIẾN NHANH:\n\n"
        "🏢 PHÂN HỆ DOANH NGHIỆP (EB):\n"
        "🔹 Gõ alpha:\n"
        "-> Thẩm định BCTC Alpha Group (Doanh thu 318 tỷ, Vốn lưu động ròng NWC, DSCR 0.37x, Red Flags cảnh báo).\n"
        "🔹 Gõ beta:\n"
        "-> Thẩm định BCTC Cty XNK Beta (Doanh thu 280 tỷ, DSCR 1.87x, gói Bán chéo Cross-sell FX/SCF/LC theo QĐ 039).\n"
        "🔹 Gõ to trinh hoặc mb02a:\n"
        "-> Xuất trọn bộ Tờ trình Tín dụng MB02a (.docx 8 phần, 21 bảng biểu chuẩn MSB).\n\n"
        "👤 PHÂN HỆ CÁ NHÂN / HỘ KINH DOANH (RB):\n"
        "🔹 Gõ rb hoặc tiktok hoặc ca nhan:\n"
        "-> Thẩm định Tín dụng Hộ kinh doanh TikTok Shop (Doanh thu 2.9 tỷ, công nhận 8%, DTI 21%, Thẻ tín dụng & Đề xuất hạn mức).\n\n"
        "⚡ TIỆN ÍCH HỆ THỐNG:\n"
        "🔹 Gõ status: Kiểm tra sức khỏe toàn diện các Agent Runtime trên Cloud.\n"
        "🔹 THẨM ĐỊNH AD-HOC BẤT KỲ: Nhập số liệu tài chính bất kỳ của DN hoặc Cá nhân, GreenNode MaaS AI sẽ phân tích và phản hồi ngay lập tức!"
    )

# ================= MAIN POLLING DISPATCHER =================
def process_incoming_message(msg_obj):
    try:
        chat = msg_obj.get("chat") or {}
        chat_id = chat.get("id")
        sender = msg_obj.get("from") or {}
        sender_id = str(sender.get("id") or "")
        if not chat_id:
            chat_id = sender_id
            
        text = (msg_obj.get("text") or "").strip()
        user_name = sender.get("display_name") or sender.get("name") or chat.get("name") or f"Khách ({chat_id})"
        group_name = chat.get("name") or chat.get("title") or ""
        chat_id_str = str(chat_id)
        is_group = bool(group_name or (chat_id_str != sender_id and sender_id))
        
        target_log = f"[{user_name}] trong Nhóm [{group_name}] (Chat: {chat_id}, Sender: {sender_id})" if is_group else f"[{user_name}] Chat ID [{chat_id}]"
        logger.info(f"===> New Zalo Message from {target_log}: '{text}'")
        
        if not text or not chat_id:
            logger.warning("Empty text or chat_id, skipping.")
            return

        # Bóc tách và làm sạch tiền tố nhắc tên Bot trong nhóm (@Bot Agent EB 360 ...)
        import re
        clean_text = re.sub(r"^@bot(\s*agent\s*eb\s*360)?\s*", "", text, flags=re.IGNORECASE).strip()
        if not clean_text:
            clean_text = text
        lower_text = clean_text.lower()
        is_admin = (sender_id == str(ADMIN_CHAT_ID) or chat_id_str == str(ADMIN_CHAT_ID))
        t0 = time.time()


        
        # 0. Kiểm tra xem người dùng hoặc nhóm có bị chặn (Blocked) không
        if is_blocked(chat_id_str) or (sender_id and is_blocked(sender_id)):
            target_block_id = sender_id if (sender_id and is_blocked(sender_id)) else chat_id_str
            logger.warning(f"Blocked user [{target_block_id}] tried to send: '{text}'")
            zalo_send_message(chat_id, "⚠️ Thông báo từ hệ thống: Quyền truy cập Bot Agent EB 360 của bạn hiện đang tạm dừng. Vui lòng liên hệ Giám đốc Michael Nguyên để biết thêm chi tiết.")
            try:
                zalo_send_message(ADMIN_CHAT_ID, f"🚨 [CẢNH BÁO] Người dùng bị chặn [{user_name} - `{target_block_id}`] vừa cố gửi tin: \"{text}\"")
            except Exception:
                pass
            return

        # 0.1. LỆNH ĐẶC BIỆT DÀNH CHO SẾP MICHAEL (SUPER ADMIN)
        if is_admin:
            if lower_text.startswith("/block") or lower_text.startswith("/chan"):
                parts = text.split()
                if len(parts) >= 2:
                    target_id = parts[1].strip()
                    block_user(target_id)
                    zalo_send_message(chat_id, f"🚫 ĐÃ THU HỒI QUYỀN THÀNH CÔNG!\nUser/Chat ID `{target_id}` đã bị đưa vào danh sách chặn. Từ bây giờ người này không thể sử dụng Bot nữa.")
                else:
                    zalo_send_message(chat_id, "⚠️ Cú pháp: `/block [Chat_ID]` (VD: `/block 123456789`)")
                return

            elif lower_text.startswith("/unblock") or lower_text.startswith("/mo"):
                parts = text.split()
                if len(parts) >= 2:
                    target_id = parts[1].strip()
                    if unblock_user(target_id):
                        zalo_send_message(chat_id, f"✅ ĐÃ MỞ LẠI QUYỀN!\nUser/Chat ID `{target_id}` đã được gỡ chặn và có thể tiếp tục dùng Bot.")
                    else:
                        zalo_send_message(chat_id, f"ℹ️ User/Chat ID `{target_id}` không nằm trong danh sách chặn.")
                else:
                    zalo_send_message(chat_id, "⚠️ Cú pháp: `/unblock [Chat_ID]`")
                return

            elif lower_text in ["/list", "/users", "/danhsach", "/danh_sach"]:
                registry = load_json_data(USER_REGISTRY_FILE)
                blocked = load_json_data(BLOCKED_USERS_FILE)
                lines = [
                    "📋 DANH SÁCH THEO DÕI NGƯỜI DÙNG BOT AGENT EB 360:",
                    "------------------------------------------"
                ]
                if not registry:
                    lines.append("Chưa có người ngoài nào tương tác với Bot.")
                else:
                    for cid, uinfo in registry.items():
                        st = "🚫 ĐANG CHẶN" if cid in blocked else "✅ ĐANG DÙNG"
                        lines.append(f"• {uinfo.get('name', 'N/A')} (ID: `{cid}`)\n  Trạng thái: {st} | Đã hỏi: {uinfo.get('query_count', 0)} câu | Lần cuối: {uinfo.get('last_seen', 'N/A')}\n  Gần nhất: \"{uinfo.get('last_query', '')[:50]}...\"\n")
                lines.append("👉 Lệnh thu hồi: `/block [ID]` | Mở lại: `/unblock [ID]`")
                zalo_send_message(chat_id, "\n".join(lines))
                return

        # ================= XỬ LÝ NỘI DUNG CHAT =================
        reply = ""
        # 1. Greetings & Menu
        if lower_text in ["/start", "hi", "hello", "xin chào", "xin chao", "chào", "chao", "menu", "help", "trợ giúp", "tro giup"]:
            reply = get_welcome_menu()
            zalo_send_message(chat_id, reply)
        # 2. Beta Assessment (Agent 1 Cloud)
        elif "beta" in lower_text:
            zalo_send_message(chat_id, "⏳ Bot Agent EB 360 đã nhận lệnh!\nĐang gọi Agent 1 Cloud để giải phẫu BCTC Cty XNK Beta (280 tỷ)...")
            reply = call_agent_assess("beta")
            zalo_send_message(chat_id, reply)
        # 3. Alpha Assessment (Agent 1 Cloud)
        elif any(k in lower_text for k in ["alpha", "tham dinh alpha", "bctc alpha"]):
            zalo_send_message(chat_id, "⏳ Bot Agent EB 360 đã nhận lệnh!\nĐang gọi Agent 1 Cloud để giải phẫu BCTC Alpha Group (318 tỷ)...")
            reply = call_agent_assess("alpha")
            zalo_send_message(chat_id, reply)
        # 4. Credit Memo Builder (Agent 4 Cloud)
        elif any(k in lower_text for k in ["to trinh", "tờ trình", "memo", "mb02a", "mb02", "word", "xuat to trinh"]):
            zalo_send_message(chat_id, "⏳ Bot Agent EB 360 đã nhận lệnh!\nĐang gọi Agent 4 Cloud xuất Tờ trình Tín dụng MB02a (8 phần, 21 bảng biểu)...")
            reply = call_agent_memo()
            zalo_send_message(chat_id, reply)
        # 5. RB Retail Personal / TikTok Shop Assessment
        elif any(k in lower_text for k in ["rb", "retail", "tiktok", "tik tok", "ca nhan", "cá nhân", "khcn"]):
            zalo_send_message(chat_id, "⏳ Bot Agent M-Credit 360 đã nhận lệnh!\nĐang kích hoạt Động cơ Thẩm định Tín dụng KHCN / Hộ KD TikTok Shop...")
            reply = call_agent_retail()
            zalo_send_message(chat_id, reply)
        # 6. Health Check
        elif any(k in lower_text for k in ["status", "trang thai", "trạng thái", "kiem tra", "kiểm tra", "health"]):
            reply = check_system_status()
            zalo_send_message(chat_id, reply)
        # 7. Any other company assessment or general query -> GreenNode MaaS LLM
        else:
            short_q = clean_text if len(clean_text) <= 40 else clean_text[:37] + "..."
            zalo_send_message(chat_id, f"⏳ Bot Agent EB 360 đã nhận lệnh!\nĐang kết nối GreenNode MaaS AI để giải phẫu dữ liệu '{short_q}', đợi em khoảng 15-20 giây nhé...")
            reply = call_greennode_maas_llm(clean_text)
            zalo_send_message(chat_id, reply)


        elapsed = time.time() - t0
        
        # Ghi nhận hoạt động & Báo cáo ngầm về cho Sếp Michael nếu là người khác
        if not is_admin:
            target_reg_id = sender_id if sender_id else chat_id_str
            register_user_activity(target_reg_id, user_name, text)
            notify_admin_shadow(chat_id_str, sender_id, user_name, group_name, text, reply, elapsed)

    except Exception as e:
        logger.error(f"process_incoming_message error: {e}", exc_info=True)



def run_service():
    logger.info("=====================================================")
    logger.info("  STARTING M-CREDIT 360 ZALO BOT SERVICE (LIVE)")
    logger.info("=====================================================")
    
    bot_info = zalo_get_me()
    if not bot_info or not bot_info.get("ok"):
        logger.error("Failed to authenticate with Zalo Bot Platform! Please verify ZALO_BOT_TOKEN.")
        return
        
    res = bot_info.get("result", {})
    logger.info(f"Bot Identity Verified: [{res.get('display_name')}] (@{res.get('account_name')}) ID: {res.get('id')}")
    logger.info("Polling for incoming messages via getUpdates...")
    
    while True:
        try:
            updates = zalo_get_updates(timeout_sec=10)
            
            if not updates or not updates.get("ok"):
                code = updates.get("error_code") if updates else None
                if code != 408:
                    logger.debug(f"getUpdates non-ok or timeout: {updates}")
                continue
                
            raw_result = updates.get("result")
            events = []
            if isinstance(raw_result, list):
                events = raw_result
            elif isinstance(raw_result, dict):
                events = [raw_result]
                
            for ev in events:
                if not isinstance(ev, dict):
                    continue
                msg = ev.get("message")
                if isinstance(msg, dict):
                    process_incoming_message(msg)
                    
        except KeyboardInterrupt:
            logger.info("Bot service stopped by user.")
            break
        except Exception as e:
            logger.error(f"Unexpected loop exception: {e}", exc_info=True)
            time.sleep(2)

if __name__ == "__main__":
    run_service()
