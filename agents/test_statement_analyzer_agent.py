import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from statement_analyzer_agent import StatementAnalyzer, StatementError


class StatementAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.agent = StatementAnalyzer()
        self.fixture = Path(__file__).parent.parent / "data_test" / "sample_statement.csv"

    def test_csv_flow_and_all_anomaly_rules(self):
        report = self.agent.analyze_file(self.fixture, assessment_id="STMT-TEST")
        self.assertEqual(report["monthly_cash_flow"][0]["total_inflow"], 800000000.0)
        self.assertEqual(report["net_eligible_income"]["eligible_inflow"], 700000000.0)
        rules = {item["rule"] for item in report["suspicious_transactions"]}
        self.assertTrue({"CASH_WITHDRAWAL", "RAPID_FUNDS_MOVEMENT", "REPEATED_ROUND_AMOUNT", "AFTER_HOURS", "SENSITIVE_KEYWORD"}.issubset(rules))
        self.assertTrue(report["risk_summary"]["manual_review_required"])

    def test_rejects_missing_transactions(self):
        with self.assertRaises(StatementError):
            self.agent.analyze({"transactions": []})


if __name__ == "__main__":
    unittest.main()
