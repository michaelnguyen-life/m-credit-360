import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from eb_credit_agent import AssessmentError, CreditAssessment, normalize_amount_to_int


class CreditAssessmentTests(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).parent.parent / "data_test" / "eb_credit_assessment_sample.json"
        self.payload = json.loads(fixture.read_text(encoding="utf-8"))

    def test_calculates_and_detects_all_five_flags(self):
        profile = CreditAssessment().assess(self.payload)
        self.assertEqual(profile["ratios"]["nwc"], -60000.0)
        self.assertEqual(profile["ratios"]["net_cash_flow"], -5000.0)
        self.assertEqual(len([flag for flag in profile["red_flags"] if flag["triggered"]]), 5)
        self.assertEqual(profile["preliminary_decision"]["outcome"], "manual_review_required")

    def test_product_039_uses_static_calculations_and_split_screen(self):
        profile = CreditAssessment().assess(self.payload)
        product = profile["product_039_evaluation"]
        self.assertEqual(product["decision"], "ĐỦ ĐIỀU KIỆN SẢN PHẨM 039")
        self.assertEqual(product["calculations"]["buyer_average_revenue_2y"], 65000000000.0)
        self.assertEqual(product["calculations"]["funding_ratio"], 0.75)
        self.assertTrue(all(rule["passed"] for rule in product["rules"]))
        self.assertIn("raw_documents", profile["split_screen_demo"])
        self.assertIn("Kết quả Thẩm định Sản phẩm Đầu ra 039", profile["one_page_credit_memo"])

    def test_amount_normalization_and_outdated_statement_flag(self):
        self.assertEqual(normalize_amount_to_int("Mười tỷ"), 10_000_000_000)
        self.assertEqual(normalize_amount_to_int("10 tỷ"), 10_000_000_000)
        self.assertEqual(normalize_amount_to_int("10,000,000,000"), 10_000_000_000)
        payload = dict(self.payload)
        payload["financial_statement_date"] = "2024-01-01"
        payload["financial_statement_valid_until"] = "2024-12-31"
        payload["assessment_date"] = "2026-01-01"
        flags = CreditAssessment().assess(payload)["red_flags"]
        outdated = next(flag for flag in flags if flag["code"] == "OUTDATED_DATA")
        self.assertTrue(outdated["triggered"])

    def test_rejects_empty_financials(self):
        with self.assertRaises(AssessmentError):
            CreditAssessment().assess({"financials": {}})


if __name__ == "__main__":
    unittest.main()
