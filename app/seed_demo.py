from __future__ import annotations

import os
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.helpers import build_request_summary
from app.models import BuyerRequest, Supplier
from app.schemas import as_display


def generate_ai_assistant_summary(request: BuyerRequest, suppliers: list[Supplier]) -> Dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "mode": "rule_based_fallback",
            "summary": "AI API key not configured. The system used the rule-based sourcing evaluation and database-only evidence.",
            "recommendations": [
                "Request missing supplier evidence or certificates before moving forward.",
                "Prioritize verified or under-review suppliers only after human validation.",
            ],
        }

    requirements = build_request_summary(request)
    matched = [supplier.company_name for supplier in suppliers]
    return {
        "mode": "ai_assisted",
        "summary": f"AI is enabled. The request for {requirements['commodity']} is being compared against {len(matched)} candidate suppliers."
        ,
        "recommendations": [
            "Review any mismatches in grade, quantity, and country match before outreach.",
            "Check evidence and certificates for each candidate before any commitment.",
        ],
    }


def risk_flags_for_supplier(supplier: Supplier) -> list[str]:
    flags: list[str] = []
    if supplier.verification_status in {"unverified", "evidence_pending"}:
        flags.append("Verification evidence is pending or incomplete.")
    if supplier.verification_status == "rejected":
        flags.append("This supplier has been rejected and should not be considered for outreach.")
    if not supplier.certificates:
        flags.append("Certificates or supporting evidence were not provided.")
    if supplier.indicative_price is None:
        flags.append("No indicative price was recorded.")
    return flags


def build_report_download_text(request: BuyerRequest, matches: list[dict], ai_summary: dict) -> str:
    lines = [
        "Africa Sourcing Agent - Sourcing Report",
        "====================================",
        f"Buyer: {request.buyer_name} ({request.company_name})",
        f"Commodity: {request.commodity}",
        f"Grade/Spec: {as_display(request.grade_or_spec, 'Unknown')}",
        f"Quantity: {as_display(request.quantity, 'Unknown')} {as_display(request.quantity_unit, 'Unknown')}",
        f"Origin: {as_display(request.origin_country, 'Unknown')}",
        f"Destination: {as_display(request.destination_country, 'Unknown')}",
        "",
        "Candidate Suppliers",
    ]

    if not matches:
        lines.append("No suitable suppliers met the minimum threshold.")
    else:
        for index, match in enumerate(matches, start=1):
            supplier = match["supplier"]
            lines.append(f"{index}. {supplier.company_name} [{supplier.verification_status}] - Score: {match['match_score']}")
            lines.append(f"   Country: {supplier.country}")
            lines.append(f"   Quantity claim: {supplier.quantity_claim or 'Unknown'}")
            lines.append(f"   Indicative price: {supplier.indicative_price or 'Unknown'} {supplier.currency or ''}")
            lines.append(f"   Source: {supplier.source_of_information}")
            lines.append(f"   Evidence: {supplier.certificates or 'Not provided'}")
            lines.append(f"   Risks: {', '.join(risk_flags_for_supplier(supplier)) if risk_flags_for_supplier(supplier) else 'None noted'}")
            lines.append("")

    lines.extend(["AI Summary:", ai_summary.get("summary", "No AI summary available."), ""])
    lines.extend(["Disclaimer:", "This report is an internal sourcing aide and does not guarantee legality, availability, or transaction completion."])
    return "\n".join(lines)
