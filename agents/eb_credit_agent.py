"""M-Credit 360 Enterprise Credit Assessment Agent.

Input is a JSON payload containing MSB-coded financial data.  The default
mapping is deliberately configurable because an approved MSB data dictionary
must be used before production credit decisions are made.
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable, Mapping


LOGGER = logging.getLogger(__name__)


# Default MSB code dictionary.
# Can be overridden via the request's ``code_map`` field.
DEFAULT_CODE_MAP: dict[str, tuple[str, ...]] = {
    "current_assets": ("BS_CURRENT_ASSETS", "CURRENT_ASSETS"),
    "current_liabilities": ("BS_CURRENT_LIABILITIES", "CURRENT_LIABILITIES"),
    "trade_receivables": ("BS_TRADE_RECEIVABLES", "TRADE_RECEIVABLES"),
    "inventory": ("BS_INVENTORY", "INVENTORY"),
    "trade_payables": ("BS_TRADE_PAYABLES", "TRADE_PAYABLES"),
    "short_term_debt": ("BS_SHORT_TERM_DEBT", "SHORT_TERM_DEBT"),
    "total_liabilities": ("BS_TOTAL_LIABILITIES", "TOTAL_LIABILITIES"),
    "equity": ("BS_EQUITY", "EQUITY"),
    "ebit": ("IS_EBIT", "EBIT"),
    "interest_expense": ("IS_INTEREST_EXPENSE", "INTEREST_EXPENSE"),
    "revenue": ("IS_REVENUE", "REVENUE"),
    "operating_cash_flow": ("CF_OPERATING_CASH_FLOW", "CFO"),
    "investing_cash_flow": ("CF_INVESTING_CASH_FLOW", "CFI"),
    "financing_cash_flow": ("CF_FINANCING_CASH_FLOW", "CFF"),
    "cash_available_for_debt_service": ("CFADS", "CASH_AVAILABLE_FOR_DEBT_SERVICE"),
    "principal_due": ("PRINCIPAL_DUE",),
}

DEFAULT_THRESHOLDS: dict[str, Decimal] = {
    "max_short_term_debt_to_liabilities": Decimal("0.50"),
    "max_dsp_variance": Decimal("0.05"),
    "min_dscr": Decimal("1.00"),
    "min_icr": Decimal("1.50"),
}


class AssessmentError(ValueError):
    """A recoverable validation error in a credit-assessment request."""


def normalize_amount_to_int(value: Any) -> int | None:
    """Convert common Vietnamese amount formats to an integer VND amount.

    This is intentionally deterministic: unsupported wording returns None
    instead of allowing a model or heuristic to infer a financial value.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, Decimal)):
        return int(value)
    if isinstance(value, float):
        return int(value) if math.isfinite(value) else None
    text = str(value).strip().lower()
    if not text:
        return None
    compact = text.replace(" ", "").replace(",", "").replace(".", "")
    if re.fullmatch(r"-?\d+", compact):
        return int(compact)
    normalized = "".join(
        char for char in unicodedata.normalize("NFD", text) if unicodedata.category(char) != "Mn"
    ).replace("đ", "d")
    normalized = re.sub(r"\b(vnd|dong|d)\b", "", normalized)
    numeric_scale = re.fullmatch(r"\s*([+-]?[\d.,]+)\s*(nghin|ngan|trieu|ty|ti)\s*", normalized)
    if numeric_scale:
        raw_number, unit = numeric_scale.groups()
        digits_only = raw_number.replace(",", "").replace(".", "")
        if re.fullmatch(r"[+-]?\d+", digits_only):
            return int(digits_only) * {"nghin": 1_000, "ngan": 1_000, "trieu": 1_000_000, "ty": 1_000_000_000, "ti": 1_000_000_000}[unit]
    tokens = re.findall(r"[a-z]+", normalized)
    digits = {"khong": 0, "mot": 1, "mots": 1, "mot": 1, "hai": 2, "ba": 3, "bon": 4, "tu": 4, "nam": 5, "lam": 5, "sau": 6, "bay": 7, "tam": 8, "chin": 9}
    scales = {"nghin": 1_000, "ngan": 1_000, "trieu": 1_000_000, "ty": 1_000_000_000, "ti": 1_000_000_000}
    if not tokens or any(token not in digits and token not in scales and token not in {"muoi", "tram", "le", "linh"} for token in tokens):
        return None
    total = 0
    group = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in scales:
            total += (group or 1) * scales[token]
            group = 0
        elif token in {"le", "linh"}:
            pass
        elif token == "muoi":
            group += 10
        elif token == "tram":
            # "mot tram" has accumulated 1; bare "tram" means one hundred.
            group = (group or 1) * 100
        else:
            digit = digits[token]
            next_token = tokens[index + 1] if index + 1 < len(tokens) else ""
            if next_token == "tram":
                group += digit * 100
                index += 1
            elif next_token == "muoi":
                group += digit * 10
                index += 1
            else:
                group += digit
        index += 1
    return total + group


def _decimal(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, Decimal):
        return value if value.is_finite() else None
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value)) if math.isfinite(value) else None
    text = str(value).strip()
    if re.search(r"[A-Za-zÀ-ỹà-ỹĐđ]", text):
        normalized = normalize_amount_to_int(text)
        return Decimal(normalized) if normalized is not None else None
    try:
        result = Decimal(text.replace(",", ""))
    except (InvalidOperation, AttributeError):
        return None
    return result if result.is_finite() else None


def _number(value: Decimal | None) -> float | None:
    return float(value) if value is not None else None


def _ratio(numerator: Decimal | None, denominator: Decimal | None) -> Decimal | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def _first_value(values: Mapping[str, Decimal], codes: Iterable[str]) -> Decimal | None:
    for code in codes:
        value = values.get(code.upper())
        if value is not None:
            return value
    return None


def _severity(level: str) -> int:
    return {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(level, 0)


def _parse_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    for layout in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, layout).date()
        except ValueError:
            continue
    return None


class Product039Evaluator:
    """Deterministic eligibility rules for MSB Product 039."""

    @staticmethod
    def buyer_average_revenue(year_1: Decimal | None, year_2: Decimal | None) -> Decimal | None:
        return (year_1 + year_2) / 2 if year_1 is not None and year_2 is not None else None

    @staticmethod
    def funding_ratio(requested_amount: Decimal | None, contract_value: Decimal | None) -> Decimal | None:
        return _ratio(requested_amount, contract_value)

    @staticmethod
    def evaluate(product: Any, equity_from_financials: Decimal | None) -> dict[str, Any]:
        source = product if isinstance(product, Mapping) else {}
        def value(*names: str) -> Decimal | None:
            for name in names:
                if name in source:
                    return _decimal(source[name])
            return None

        customer_years = value("customer_operating_years", "SoNamHoatDong")
        customer_equity = value("customer_equity", "VCSH") or equity_from_financials
        buyer_years = value("buyer_operating_years", "SoNamHoatDong_Buyer")
        buyer_year_1 = value("buyer_revenue_year_1", "DT_Nam_1")
        buyer_year_2 = value("buyer_revenue_year_2", "DT_Nam_2")
        buyer_average = Product039Evaluator.buyer_average_revenue(buyer_year_1, buyer_year_2)
        provided_average = value("buyer_avg_revenue_2y", "DT_BQ_2Nam")
        requested_amount = value("loan_request_amount", "DeNghi_TaiTro")
        contract_value = value("contract_value", "GiaTri_HDDR")
        ratio = Product039Evaluator.funding_ratio(requested_amount, contract_value)

        def rule(code: str, title: str, passed: bool, evidence: str) -> dict[str, Any]:
            return {"code": code, "title": title, "status": "PASS" if passed else "RED FLAG", "passed": passed, "evidence": evidence}

        customer_passed = customer_years is not None and customer_equity is not None and customer_years >= 3 and customer_equity > 0
        buyer_passed = buyer_average is not None and buyer_years is not None and buyer_average >= Decimal("50000000000") and buyer_years >= 3
        funding_passed = ratio is not None and ratio <= Decimal("0.8")
        rules = [
            rule("P039_R1_CUSTOMER", "Tư cách Khách hàng", customer_passed, f"SoNamHoatDong={_number(customer_years)}; VCSH={_number(customer_equity)}; yêu cầu >=3 năm và VCSH > 0."),
            rule("P039_R2_BUYER", "Tư cách Người mua", buyer_passed, f"DT_BQ_2Nam={_number(buyer_average)}; SoNamHoatDong_Buyer={_number(buyer_years)}; yêu cầu DT_BQ >= 50 tỷ và >=3 năm."),
            rule("P039_R3_FUNDING_RATIO", "Tỷ lệ tài trợ", funding_passed, f"TyLeTaiTro={_number(ratio)}; yêu cầu <= 0.80."),
        ]
        warnings = []
        if provided_average is not None and buyer_average is not None and provided_average != buyer_average:
            warnings.append("Buyer average revenue supplied in payload differs from the deterministic two-year calculation.")
        if buyer_average is None:
            warnings.append("Buyer eligibility requires buyer_revenue_year_1 and buyer_revenue_year_2; a pre-calculated average is not accepted as primary evidence.")
        return {
            "product": "039",
            "decision": "ĐỦ ĐIỀU KIỆN SẢN PHẨM 039" if all(item["passed"] for item in rules) else "TỪ CHỐI / YÊU CẦU NGOẠI LỆ",
            "rules": rules,
            "calculations": {"buyer_revenue_year_1": _number(buyer_year_1), "buyer_revenue_year_2": _number(buyer_year_2), "buyer_average_revenue_2y": _number(buyer_average), "funding_ratio": _number(ratio), "loan_request_amount": _number(requested_amount), "contract_value": _number(contract_value)},
            "warnings": warnings,
        }


@dataclass
class CreditAssessment:
    """Deterministic credit assessment, independent of an LLM provider."""

    code_map: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: dict(DEFAULT_CODE_MAP)
    )
    thresholds: dict[str, Decimal] = field(
        default_factory=lambda: dict(DEFAULT_THRESHOLDS)
    )

    def assess(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, Mapping):
            raise AssessmentError("Payload must be a JSON object.")

        warnings: list[str] = []
        values = self._normalize_financials(payload, warnings)
        code_map = self._effective_code_map(payload.get("code_map"), warnings)
        thresholds = self._effective_thresholds(payload.get("thresholds"), warnings)
        metrics = {
            name: _first_value(values, codes) for name, codes in code_map.items()
        }
        self._overlay_explicit_debt_service(metrics, payload.get("debt_service"), warnings)
        ratios, calculation_notes = self._calculate(metrics)
        flags = self._red_flags(metrics, ratios, payload.get("dsp"), thresholds, warnings)
        freshness_flag = self._financial_statement_freshness(payload, warnings)
        flags.append(freshness_flag)
        product_039 = Product039Evaluator.evaluate(payload.get("product_039"), metrics.get("equity"))
        warnings.extend(product_039["warnings"])
        decision = self._preliminary_decision(flags, warnings)

        supply_chain = self._supply_chain_analysis(payload.get("supply_chain"))
        anomaly_summary = self._statement_anomaly_summary(payload.get("statement_analysis"))
        deep_dive = self._financial_deep_dive(metrics, ratios, flags)
        swot = self._swot_analysis(metrics, ratios, flags, product_039, supply_chain, anomaly_summary)
        covenants = self._credit_covenants(flags, product_039, decision)

        profile = {
            "schema_version": "1.0",
            "assessment_id": str(payload.get("assessment_id") or self._assessment_id()),
            "assessed_at": datetime.now(timezone.utc).isoformat(),
            "status": "completed_with_warnings" if warnings else "completed",
            "company": self._company(payload.get("company")),
            "reporting_period": payload.get("reporting_period"),
            "currency": payload.get("currency", "VND"),
            "source": {"type": payload.get("source_type", "json"), "codes_received": sorted(values)},
            "normalized_financials": {code: _number(value) for code, value in values.items()},
            "metrics": {name: _number(value) for name, value in metrics.items()},
            "ratios": {name: _number(value) for name, value in ratios.items()},
            "calculation_notes": calculation_notes,
            "red_flags": flags,
            "product_039_evaluation": product_039,
            "supply_chain_analysis": supply_chain,
            "statement_anomaly_summary": anomaly_summary,
            "financial_deep_dive": deep_dive,
            "swot_analysis": swot,
            "credit_covenants": covenants,
            "thresholds": {name: _number(value) for name, value in thresholds.items()},
            "preliminary_decision": decision,
            "warnings": warnings,
            "errors": [],
        }
        profile["split_screen_demo"] = self._split_screen(payload, profile)
        profile["one_page_credit_memo"] = self.render_memo(profile)
        return profile

    def assess_file(self, path: str | Path) -> dict[str, Any]:
        """Assess a JSON file or extract code/value pairs from a text PDF."""
        source = Path(path)
        if not source.is_file():
            raise AssessmentError(f"Input file does not exist: {source}")
        suffix = source.suffix.lower()
        if suffix == ".json":
            try:
                payload = json.loads(source.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AssessmentError(f"Invalid JSON input: {exc}") from exc
            if not isinstance(payload, dict):
                raise AssessmentError("JSON input must contain one object.")
            payload.setdefault("source_type", "json")
            return self.assess(payload)
        if suffix == ".pdf":
            return self.assess({"financials": self.extract_pdf(source), "source_type": "pdf"})
        raise AssessmentError("Supported input formats are .json and text-based .pdf.")

    def extract_pdf(self, path: str | Path) -> dict[str, Decimal]:
        """Extract ``MSB_CODE amount`` patterns. Scanned PDFs require OCR upstream."""
        try:
            from pypdf import PdfReader  # type: ignore[import-not-found]
        except ImportError as exc:
            raise AssessmentError("PDF support requires installing pypdf.") from exc
        try:
            text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        except Exception as exc:  # pypdf raises several parsing exception types
            raise AssessmentError(f"Could not read PDF: {exc}") from exc
        if not text.strip():
            raise AssessmentError("PDF has no extractable text; OCR is required for scanned documents.")
        found: dict[str, Decimal] = {}
        pattern = re.compile(r"\b([A-Z]{2,4}\d{3,}|[A-Z][A-Z_]{2,})\b\s*[:|]?\s*\(?(-?[\d,.]+)\)?")
        for code, raw_value in pattern.findall(text.upper()):
            value = _decimal(raw_value)
            if value is not None:
                found[code] = -value if raw_value.strip().startswith("(") else value
        if not found:
            raise AssessmentError("No MSB code/value pairs were found in the PDF text.")
        return found

    def write_outputs(self, profile: Mapping[str, Any], output_dir: str | Path = "output_memos") -> tuple[Path, Path]:
        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        identifier = re.sub(r"[^A-Za-z0-9_.-]", "_", str(profile["assessment_id"]))
        json_path = directory / f"{identifier}.credit_profile.json"
        memo_path = directory / f"{identifier}.credit_memo.md"
        json_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        memo_path.write_text(str(profile["one_page_credit_memo"]), encoding="utf-8")
        return json_path, memo_path

    def _normalize_financials(self, payload: Mapping[str, Any], warnings: list[str]) -> dict[str, Decimal]:
        raw = payload.get("financials", payload.get("statements", {}))
        if not isinstance(raw, Mapping):
            raise AssessmentError("financials must be an object keyed by MSB code.")
        values: dict[str, Decimal] = {}
        for code, value in self._flatten_financials(raw):
            numeric = _decimal(value)
            if numeric is None:
                warnings.append(f"Ignored non-numeric value for code {code}.")
                continue
            normalized_code = str(code).upper().strip()
            if normalized_code in values:
                warnings.append(f"Duplicate code {normalized_code}; last numeric value was used.")
            values[normalized_code] = numeric
        if not values:
            raise AssessmentError("No usable financial values were supplied.")
        return values

    @staticmethod
    def _flatten_financials(raw: Mapping[str, Any]) -> Iterable[tuple[str, Any]]:
        for code, value in raw.items():
            if isinstance(value, Mapping):
                if "value" in value:
                    yield str(code), value["value"]
                else:
                    yield from CreditAssessment._flatten_financials(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Mapping) and "code" in item and "value" in item:
                        yield str(item["code"]), item["value"]
            else:
                yield str(code), value

    def _effective_code_map(self, custom: Any, warnings: list[str]) -> dict[str, tuple[str, ...]]:
        effective = dict(self.code_map)
        if custom is None:
            return effective
        if not isinstance(custom, Mapping):
            warnings.append("Ignored code_map because it is not an object.")
            return effective
        for metric, codes in custom.items():
            candidates = [codes] if isinstance(codes, str) else codes
            if not isinstance(candidates, list) or not all(isinstance(code, str) for code in candidates):
                warnings.append(f"Ignored invalid code_map entry for {metric}.")
                continue
            effective[str(metric)] = tuple(candidates)
        return effective

    def _effective_thresholds(self, custom: Any, warnings: list[str]) -> dict[str, Decimal]:
        effective = dict(self.thresholds)
        if custom is None:
            return effective
        if not isinstance(custom, Mapping):
            warnings.append("Ignored thresholds because it is not an object.")
            return effective
        for name, value in custom.items():
            numeric = _decimal(value)
            if numeric is None or numeric < 0:
                warnings.append(f"Ignored invalid threshold {name}.")
            else:
                effective[str(name)] = numeric
        return effective

    @staticmethod
    def _overlay_explicit_debt_service(metrics: dict[str, Decimal | None], raw: Any, warnings: list[str]) -> None:
        if raw is None:
            return
        if not isinstance(raw, Mapping):
            warnings.append("Ignored debt_service because it is not an object.")
            return
        for key in ("principal_due", "cash_available_for_debt_service", "interest_expense"):
            if key in raw:
                value = _decimal(raw[key])
                if value is None:
                    warnings.append(f"Ignored non-numeric debt_service.{key}.")
                else:
                    metrics[key] = value

    @staticmethod
    def _calculate(metrics: Mapping[str, Decimal | None]) -> tuple[dict[str, Decimal | None], list[str]]:
        notes: list[str] = []
        nwc = None
        if metrics.get("current_assets") is not None and metrics.get("current_liabilities") is not None:
            nwc = metrics["current_assets"] - metrics["current_liabilities"]  # type: ignore[operator]
        else:
            notes.append("NWC requires current_assets and current_liabilities.")
        wcr = None
        if all(metrics.get(key) is not None for key in ("trade_receivables", "inventory", "trade_payables")):
            wcr = metrics["trade_receivables"] + metrics["inventory"] - metrics["trade_payables"]  # type: ignore[operator]
        else:
            notes.append("WCR requires trade_receivables, inventory and trade_payables.")
        net_cash_flow = None
        if all(metrics.get(key) is not None for key in ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow")):
            net_cash_flow = metrics["operating_cash_flow"] + metrics["investing_cash_flow"] + metrics["financing_cash_flow"]  # type: ignore[operator]
        else:
            notes.append("Net cash flow requires operating, investing and financing cash flow.")
        cfads = metrics.get("cash_available_for_debt_service") or metrics.get("operating_cash_flow")
        if metrics.get("cash_available_for_debt_service") is None and cfads is not None:
            notes.append("DSCR uses operating_cash_flow as CFADS proxy.")
        debt_service = None
        if metrics.get("principal_due") is not None and metrics.get("interest_expense") is not None:
            debt_service = metrics["principal_due"] + metrics["interest_expense"]  # type: ignore[operator]
        dscr = _ratio(cfads, debt_service)
        icr = _ratio(metrics.get("ebit"), metrics.get("interest_expense"))
        return {"nwc": nwc, "wcr": wcr, "dscr": dscr, "icr": icr, "net_cash_flow": net_cash_flow}, notes

    def _red_flags(self, metrics: Mapping[str, Decimal | None], ratios: Mapping[str, Decimal | None], dsp: Any, thresholds: Mapping[str, Decimal], warnings: list[str]) -> list[dict[str, Any]]:
        flags: list[dict[str, Any]] = []
        def add(code: str, title: str, triggered: bool, severity: str, observed: Decimal | None, threshold: Decimal | None, evidence: str) -> None:
            flags.append({"code": code, "title": title, "triggered": triggered, "severity": severity if triggered else "none", "observed_value": _number(observed), "threshold": _number(threshold), "evidence": evidence})

        capital_imbalance = (metrics.get("equity") is not None and metrics["equity"] <= 0) or (ratios.get("nwc") is not None and ratios["nwc"] < 0)
        add("RF01_CAPITAL_IMBALANCE", "Mất cân đối vốn", capital_imbalance, "high", ratios.get("nwc"), Decimal("0"), "Equity <= 0 or NWC < 0.")
        cfo = metrics.get("operating_cash_flow")
        add("RF02_NEGATIVE_CFO", "Dòng tiền HĐKD âm", cfo is not None and cfo < 0, "high", cfo, Decimal("0"), "Operating cash flow is below zero.")
        short_debt_ratio = _ratio(metrics.get("short_term_debt"), metrics.get("total_liabilities"))
        short_threshold = thresholds["max_short_term_debt_to_liabilities"]
        add("RF03_SHORT_TERM_DEBT", "Nợ ngắn hạn vượt ngưỡng", short_debt_ratio is not None and short_debt_ratio > short_threshold, "medium", short_debt_ratio, short_threshold, "Short-term debt / total liabilities exceeds policy threshold.")
        dsp_variance = self._dsp_variance(metrics, dsp, warnings)
        dsp_threshold = thresholds["max_dsp_variance"]
        add("RF04_DSP_MISMATCH", "Lệch số liệu Digisale (DSP)", dsp_variance is not None and dsp_variance > dsp_threshold, "high", dsp_variance, dsp_threshold, "Largest relative variance for revenue or trade receivables.")
        dscr, icr = ratios.get("dscr"), ratios.get("icr")
        weak_debt_service = (dscr is not None and dscr < thresholds["min_dscr"]) or (icr is not None and icr < thresholds["min_icr"])
        observed = dscr if dscr is not None else icr
        add("RF05_DEBT_SERVICE_CAPACITY", "Khả năng trả nợ yếu", weak_debt_service, "critical", observed, thresholds["min_dscr"], "DSCR < minimum or ICR < minimum.")
        return flags

    @staticmethod
    def _financial_statement_freshness(payload: Mapping[str, Any], warnings: list[str]) -> dict[str, Any]:
        assessment_date = _parse_date(payload.get("assessment_date")) or datetime.now(timezone.utc).date()
        statement_date = _parse_date(payload.get("financial_statement_date") or payload.get("reporting_period_end"))
        valid_until = _parse_date(payload.get("financial_statement_valid_until"))
        reasons: list[str] = []
        if statement_date is None:
            warnings.append("Missing or invalid financial_statement_date; BCTC freshness could not be fully verified.")
        elif (assessment_date - statement_date).days > 365:
            reasons.append("Financial statement date is more than 12 months before assessment date.")
        if valid_until is not None and valid_until < assessment_date:
            reasons.append("financial_statement_valid_until has expired.")
        return {"code": "OUTDATED_DATA", "title": "Dữ liệu BCTC quá hạn", "triggered": bool(reasons), "severity": "medium" if reasons else "none", "observed_value": statement_date.isoformat() if statement_date else None, "threshold": "12 months / valid-until", "evidence": " ".join(reasons) if reasons else "Financial statement is within the 12-month policy window and has not expired."}

    @staticmethod
    def _split_screen(payload: Mapping[str, Any], profile: Mapping[str, Any]) -> dict[str, Any]:
        supplied = payload.get("raw_documents")
        raw = dict(supplied) if isinstance(supplied, Mapping) else {}
        documents = {
            "financial_statement_excerpt": raw.get("financial_statement_excerpt"),
            "principle_contract_excerpt": raw.get("principle_contract_excerpt"),
        }
        ratios = profile["ratios"]
        product = profile["product_039_evaluation"]
        insights = [
            {"type": "financial_ratio", "label": "NWC", "value": ratios["nwc"]},
            {"type": "financial_ratio", "label": "DSCR", "value": ratios["dscr"]},
            {"type": "financial_ratio", "label": "ICR", "value": ratios["icr"]},
        ]
        insights.extend({"type": "financial_red_flag", "label": flag["title"], "status": "RED FLAG" if flag["triggered"] else "PASS", "evidence": flag["evidence"]} for flag in profile["red_flags"])
        insights.extend({"type": "product_039_rule", "label": rule["title"], "status": rule["status"], "evidence": rule["evidence"]} for rule in product["rules"])
        insights.append({"type": "product_039_decision", "label": "Kết quả Sản phẩm 039", "status": product["decision"]})
        return {"raw_documents": documents, "ai_extracted_insights": insights}

    @staticmethod
    def _dsp_variance(metrics: Mapping[str, Decimal | None], dsp: Any, warnings: list[str]) -> Decimal | None:
        if dsp is None:
            warnings.append("DSP data not supplied; RF04 could not be assessed.")
            return None
        if not isinstance(dsp, Mapping):
            warnings.append("DSP data is not an object; RF04 could not be assessed.")
            return None
        checks = (("revenue", metrics.get("revenue")), ("trade_receivables", metrics.get("trade_receivables")))
        variances: list[Decimal] = []
        for name, financial_value in checks:
            dsp_value = _decimal(dsp.get(name))
            if financial_value is not None and dsp_value is not None and financial_value != 0:
                variances.append(abs(financial_value - dsp_value) / abs(financial_value))
        if not variances:
            warnings.append("DSP comparison requires matching revenue or trade_receivables values.")
            return None
        return max(variances)

    @staticmethod
    def _preliminary_decision(flags: list[Mapping[str, Any]], warnings: list[str]) -> dict[str, Any]:
        triggered = [flag for flag in flags if flag["triggered"]]
        maximum = max((_severity(str(flag["severity"])) for flag in triggered), default=0)
        if maximum >= 4:
            outcome = "manual_review_required"
        elif maximum >= 3:
            outcome = "enhanced_due_diligence"
        elif maximum:
            outcome = "conditional_review"
        else:
            outcome = "no_rule_based_red_flag"
        return {"outcome": outcome, "is_automated_credit_decision": False, "triggered_flag_count": len(triggered), "data_quality_warning_count": len(warnings)}

    @staticmethod
    def _company(raw: Any) -> dict[str, Any]:
        return dict(raw) if isinstance(raw, Mapping) else {"name": None, "tax_id": None}

    @staticmethod
    def _assessment_id() -> str:
        return f"EB-{datetime.now(timezone.utc):%Y%m%d%H%M%S}"

    @staticmethod
    def _supply_chain_analysis(raw: Any) -> dict[str, Any]:
        """Analyze top-5 supplier and buyer concentration risk."""
        source = raw if isinstance(raw, Mapping) else {}
        suppliers = source.get("top_suppliers", []) if isinstance(source.get("top_suppliers"), list) else []
        buyers = source.get("top_buyers", []) if isinstance(source.get("top_buyers"), list) else []
        top_supplier_ratio = sum(_decimal(s.get("ratio")) or Decimal(0) for s in suppliers if isinstance(s, Mapping))
        top_buyer_ratio = sum(_decimal(b.get("ratio")) or Decimal(0) for b in buyers if isinstance(b, Mapping))
        supplier_concentration = "Cao" if top_supplier_ratio > Decimal("0.60") else ("Trung bình" if top_supplier_ratio > Decimal("0.40") else "Thấp")
        buyer_concentration = "Cao" if top_buyer_ratio > Decimal("0.60") else ("Trung bình" if top_buyer_ratio > Decimal("0.40") else "Thấp")
        return {
            "top_suppliers": suppliers,
            "top_buyers": buyers,
            "top5_supplier_ratio": _number(top_supplier_ratio),
            "top5_buyer_ratio": _number(top_buyer_ratio),
            "supplier_concentration": supplier_concentration,
            "buyer_concentration": buyer_concentration,
        }

    @staticmethod
    def _statement_anomaly_summary(raw: Any) -> dict[str, Any]:
        """Summarize bank-statement anomaly flags."""
        source = raw if isinstance(raw, Mapping) else {}
        anomalies = source.get("anomalies", []) if isinstance(source.get("anomalies"), list) else []
        triggered = [a for a in anomalies if isinstance(a, Mapping) and a.get("triggered")]
        max_severity = max((_severity(str(a.get("severity", "none"))) for a in triggered), default=0)
        return {
            "total_inflow": _number(_decimal(source.get("total_inflow"))),
            "total_outflow": _number(_decimal(source.get("total_outflow"))),
            "average_monthly_balance": _number(_decimal(source.get("average_monthly_balance"))),
            "months_analyzed": source.get("months_analyzed"),
            "anomalies": anomalies,
            "triggered_count": len(triggered),
            "max_severity": max_severity,
        }

    @staticmethod
    def _financial_deep_dive(metrics: Mapping[str, Decimal | None], ratios: Mapping[str, Decimal | None], flags: list[Mapping[str, Any]]) -> dict[str, Any]:
        """Generate qualitative deep-dive commentary on financial health."""
        nwc = ratios.get("nwc")
        dscr = ratios.get("dscr")
        icr = ratios.get("icr")
        cfo = metrics.get("operating_cash_flow")
        revenue = metrics.get("revenue")
        net_profit = metrics.get("net_profit") or _first_value(metrics, ("IS_NET_PROFIT", "NET_PROFIT"))
        equity = metrics.get("equity")
        current_assets = metrics.get("current_assets")
        current_liabilities = metrics.get("current_liabilities")
        current_ratio = _ratio(current_assets, current_liabilities)
        de_ratio = _ratio(metrics.get("total_liabilities"), equity)
        net_margin = _ratio(net_profit, revenue)
        roe = _ratio(net_profit, equity)
        assessments: list[dict[str, str]] = []
        assessments.append({
            "area": "Thanh khoản & Vốn lưu động",
            "observation": f"NWC = {_number(nwc)} VND; Current ratio = {_number(current_ratio)}x",
            "assessment": "Chưa đủ cơ sở đánh giá" if nwc is None else ("Đạt ngưỡng thanh khoản cơ bản" if nwc > 0 else "NWC âm — cảnh báo thanh khoản"),
        })
        assessments.append({
            "area": "Khả năng trả nợ",
            "observation": f"DSCR = {_number(dscr)}x; ICR = {_number(icr)}x",
            "assessment": "Chưa đủ cơ sở đánh giá" if dscr is None else ("CẢNH BÁO ĐỎ: DSCR dưới 1.0x — mất khả năng trả nợ từ HĐKD chính. Hệ thống YÊU CẦU Thẩm định Bổ sung nguồn thu/TSĐB và KHÔNG TỰ ĐỘNG PHÊ DUYỆT cấp vốn." if dscr < 1 else "Đạt ngưỡng trả nợ"),
        })
        assessments.append({
            "area": "Hiệu quả hoạt động",
            "observation": f"Biên lãi ròng = {_number(net_margin)}; ROE = {_number(roe)}",
            "assessment": "Chưa đủ cơ sở đánh giá" if net_margin is None else ("Biên lợi nhuận rất mỏng — rủi ro biến động doanh thu" if net_margin < Decimal("0.01") else "Biên lợi nhuận chấp nhận được"),
        })
        assessments.append({
            "area": "Đòn bẩy tài chính",
            "observation": f"D/E = {_number(de_ratio)}x",
            "assessment": "Chưa đủ cơ sở đánh giá" if de_ratio is None else ("Đòn bẩy thấp — room vay còn dư" if de_ratio < Decimal("1.0") and dscr is not None and dscr >= 1 else ("Cảnh báo: Đòn bẩy thấp nhưng dòng tiền (DSCR) không bù đắp được" if de_ratio < Decimal("1.0") else "Đòn bẩy cao — hạn chế vay thêm")),
        })
        assessments.append({
            "area": "Dòng tiền HĐKD",
            "observation": f"CFO = {_number(cfo)} VND",
            "assessment": "Chưa đủ cơ sở đánh giá" if cfo is None else ("Dòng tiền HĐKD dương — tích cực" if cfo > 0 else "Dòng tiền HĐKD âm — cảnh báo"),
        })
        return {"assessments": assessments, "current_ratio": _number(current_ratio), "de_ratio": _number(de_ratio), "net_margin": _number(net_margin), "roe": _number(roe)}

    @staticmethod
    def _swot_analysis(metrics: Mapping[str, Decimal | None], ratios: Mapping[str, Decimal | None], flags: list[Mapping[str, Any]], product_039: Mapping[str, Any], supply_chain: Mapping[str, Any], anomaly_summary: Mapping[str, Any]) -> dict[str, Any]:
        """Generate 360-degree SWOT for credit evaluation."""
        triggered_flags = [f for f in flags if isinstance(f, Mapping) and f.get("triggered")]
        nwc = ratios.get("nwc")
        dscr = ratios.get("dscr")
        cfo = metrics.get("operating_cash_flow")
        equity = metrics.get("equity")
        strengths: list[str] = []
        weaknesses: list[str] = []
        opportunities: list[str] = []
        threats: list[str] = []
        if nwc is not None and nwc > 0:
            strengths.append(f"NWC dương ({_number(nwc)} VND) — vốn lưu động dồi dào")
        if equity is not None and equity > 0:
            strengths.append(f"Vốn chủ sở hữu lớn ({_number(equity)} VND)")
        if cfo is not None and cfo > 0:
            strengths.append(f"Dòng tiền HĐKD dương ({_number(cfo)} VND)")
        if supply_chain.get("supplier_concentration") == "Thấp":
            strengths.append("Phân bổ nhà cung cấp đa dạng — rủi ro đứt nguồn thấp")
        if dscr is not None and dscr < 1:
            weaknesses.append(f"DSCR thấp ({_number(dscr)}x) — không đủ phục vụ nợ")
        icr = ratios.get("icr")
        if icr is not None and icr < Decimal("1.5"):
            weaknesses.append(f"ICR dưới ngưỡng ({_number(icr)}x)")
        net_margin = _ratio(metrics.get("net_profit") or _first_value(metrics, ("IS_NET_PROFIT", "NET_PROFIT")), metrics.get("revenue"))
        if net_margin is not None and net_margin < Decimal("0.01"):
            weaknesses.append(f"Biên lợi nhuận rất mỏng ({_number(net_margin)})")
        if supply_chain.get("buyer_concentration") in ("Cao", "Trung bình"):
            weaknesses.append(f"Tập trung khách hàng ({supply_chain.get('buyer_concentration')})")
        if anomaly_summary.get("triggered_count", 0) > 0:
            weaknesses.append(f"{anomaly_summary['triggered_count']} anomaly flag(s) từ phân tích sao kê")
        opportunities.append("Room vay còn dư (D/E thấp) — tiềm năng cấp thêm HMTD")
        opportunities.append("Sản phẩm 039 — tài trợ theo HDDR nếu bổ sung hồ sơ người mua")
        opportunities.append("Ngành BĐS phục hồi — cơ hội gia tăng doanh thu")
        for flag in triggered_flags:
            threats.append(f"{flag.get('code')}: {flag.get('title')}")
        if product_039.get("decision", "").startswith("TỪ CHỐI"):
            threats.append("Product 039 bị từ chối — yêu cầu bổ sung ngoại lệ")
        if anomaly_summary.get("max_severity", 0) >= 3:
            threats.append("Anomaly severity cao — rủi ro gian lận dòng tiền")
        threats.append("Biến động lãi suất — ảnh hưởng chi phí vốn")
        return {"strengths": strengths, "weaknesses": weaknesses, "opportunities": opportunities, "threats": threats}

    @staticmethod
    def _credit_covenants(flags: list[Mapping[str, Any]], product_039: Mapping[str, Any], decision: Mapping[str, Any]) -> dict[str, Any]:
        """Generate conditions precedent and subsequent (credit covenants)."""
        triggered = [f for f in flags if isinstance(f, Mapping) and f.get("triggered")]
        conditions_precedent: list[str] = [
            "KH cung cấp BCTC quý gần nhất đã kiểm toán",
            "Xác minh CCCD và ĐKKD bản gốc",
            "Kiểm tra dư nợ CIC tại thời điểm cấp",
            "Đăng ký giao dịch bảo đảm trên CSDLQG",
            "Phê duyệt cơ cấu tài trợ theo chính sách MSB hiện hành",
        ]
        if any(f.get("code") == "RF05_DEBT_SERVICE_CAPACITY" for f in triggered):
            conditions_precedent.append("Bổ sung phương án cải thiện DSCR (kế hoạch kinh doanh / cam kết dòng tiền)")
        if product_039.get("decision", "").startswith("TỪ CHỐI"):
            conditions_precedent.append("Bổ sung hồ sơ người mua: BCTC 2 năm gần nhất, hợp đồng nguyên tắc")
        conditions_subsequent: list[str] = [
            "Báo cáo tài chính quý (trong 30 ngày kể từ cuối quý)",
            "Giám sát dòng tiền qua tài khoản tại MSB 6 tháng/lần",
            "Kiểm tra CIC 6 tháng/lần — duy trì nhóm nợ 1",
            "Báo cáo tiến độ HDDR (đối với Product 039)",
        ]
        if any(f.get("code") == "ANM01_LARGE_CASH_WITHDRAWAL" for f in triggered):
            conditions_subsequent.append("Giới hạn rút tiền mặt không quá 5 tỷ/lần")
        if decision.get("outcome") == "manual_review_required":
            conditions_subsequent.append("Phê duyệt Hội sở — yêu cầu hồ sơ trình cấp có thẩm quyền")
        return {"conditions_precedent": conditions_precedent, "conditions_subsequent": conditions_subsequent}

    @staticmethod
    def render_memo(profile: Mapping[str, Any]) -> str:
        company = profile["company"]
        ratios = profile["ratios"]
        flags = [flag for flag in profile["red_flags"] if flag["triggered"]]
        product = profile["product_039_evaluation"]
        lines = [
            "# One-Page Credit Memo",
            f"**Doanh nghiệp:** {company.get('name') or 'Chưa cung cấp'}  ",
            f"**MST:** {company.get('tax_id') or 'Chưa cung cấp'}  ",
            f"**Kỳ báo cáo:** {profile.get('reporting_period') or 'Chưa cung cấp'}  ",
            f"**Kết quả sơ bộ:** {profile['preliminary_decision']['outcome']}",
            "", "## 1. Sức khỏe Tài chính BCTC", "| NWC | WCR | DSCR | ICR | Dòng tiền thuần |", "|---:|---:|---:|---:|---:|",
            f"| {ratios.get('nwc')} | {ratios.get('wcr')} | {ratios.get('dscr')} | {ratios.get('icr')} | {ratios.get('net_cash_flow')} |",
            "", "### Red Flags",
        ]
        lines.extend(f"- [{flag['severity'].upper()}] {flag['title']}: {flag['evidence']}" for flag in flags) if flags else lines.append("- Không phát hiện red flag theo bộ quy tắc hiện hành.")
        lines.extend(["", "## 2. Kết quả Thẩm định Sản phẩm Đầu ra 039"])
        lines.extend(f"- [{rule['status']}] {rule['title']}: {rule['evidence']}" for rule in product["rules"])
        lines.append(f"- **Quyết định 039:** {product['decision']}")
        lines.extend(["", "## 3. Khuyến nghị cấp tín dụng", "Kết quả chỉ hỗ trợ thẩm định. Chuyên viên tín dụng cần xác minh chứng từ gốc, dữ liệu DSP, điều kiện Product 039 và áp dụng chính sách MSB hiện hành trước khi phê duyệt."])
        return "\n".join(lines) + "\n"


class _RequestHandler(BaseHTTPRequestHandler):
    agent = CreditAssessment()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") == "/health":
            self._send(HTTPStatus.OK, {"status": "ok", "agent": "eb-credit-assessment"})
        else:
            self._send(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") not in {"/invocations", "/assess"}:
            self._send(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 10_000_000:
                raise AssessmentError("Request body must be between 1 byte and 10 MB.")
            request = json.loads(self.rfile.read(length).decode("utf-8"))
            payload = request.get("input", request) if isinstance(request, dict) else request
            profile = self.agent.assess(payload)
            self._send(HTTPStatus.OK, profile)
        except (AssessmentError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            self._send(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception:  # Do not disclose internals to callers.
            LOGGER.exception("Unexpected credit assessment failure")
            self._send(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Internal assessment error"})

    def _send(self, status: HTTPStatus, body: Mapping[str, Any]) -> None:
        encoded = json.dumps(body, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        LOGGER.info("%s - %s", self.address_string(), format % args)


def run_server() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), _RequestHandler)
    LOGGER.info("EB Credit Assessment Agent listening on port %s", port)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
