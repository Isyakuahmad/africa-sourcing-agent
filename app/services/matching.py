from __future__ import annotations

import os
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.helpers import get_supplier_commodities, normalize_text
from app.models import BuyerRequest, Supplier


def match_suppliers(db: Session, request: BuyerRequest) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    request_commodity = normalize_text(request.commodity)
    request_spec = normalize_text(request.grade_or_spec)
    request_origin = normalize_text(request.origin_country)
    request_destination = normalize_text(request.destination_country)

    for supplier in db.query(Supplier).all():
        supplier_commodities = get_supplier_commodities(supplier)
        commodity_match = any(normalize_text(item) in request_commodity or request_commodity in normalize_text(item) for item in supplier_commodities) or not supplier_commodities
        spec_match = bool(
            not request_spec
            or not supplier.specification
            or request_spec in normalize_text(supplier.specification)
        )
        origin_match = bool(not request_origin or not supplier.country or request_origin in normalize_text(supplier.country) or normalize_text(supplier.country) in request_origin)
        quantity_match = bool(
            not request.quantity
            or not supplier.quantity_claim
            or normalize_text(request.quantity) in normalize_text(supplier.quantity_claim)
            or normalize_text(supplier.quantity_claim) in normalize_text(request.quantity)
        )

        score = 0
        reasons: List[str] = []
        if commodity_match:
            score += 40
            reasons.append("Commodity matches buyer request.")
        else:
            reasons.append("Commodity mismatch or not supplied.")
        if spec_match:
            score += 20
            reasons.append("Specification is consistent with request.")
        else:
            reasons.append("Specification differs from requirement.")
        if origin_match:
            score += 15
            reasons.append("Origin geography is compatible.")
        else:
            reasons.append("Origin country not aligned.")
        if quantity_match:
            score += 15
            reasons.append("Quantity claim is compatible.")
        else:
            reasons.append("Quantity claim does not clearly match.")

        if supplier.verification_status == "verified":
            score += 10
            reasons.append("Supplier is verified and evidence has been reviewed.")
        elif supplier.verification_status == "under_review":
            score += 5
            reasons.append("Supplier is under review; further evidence may still be required.")
        elif supplier.verification_status in {"evidence_pending", "unverified"}:
            score -= 10
            reasons.append("Verification evidence is still pending or incomplete.")
        elif supplier.verification_status == "rejected":
            score -= 25
            reasons.append("Supplier was rejected and should not be treated as a viable candidate.")

        if score < 35:
            continue

        candidates.append(
            {
                "supplier": supplier,
                "match_score": score,
                "reasons": reasons,
                "is_viable": score >= 45,
                "verification_status": supplier.verification_status,
                "data_quality": "solid" if supplier.verification_status == "verified" else "needs-review",
            }
        )

    return sorted(candidates, key=lambda item: item["match_score"], reverse=True)


def generate_report(db: Session, request: BuyerRequest) -> Dict[str, Any]:
    candidates = match_suppliers(db, request)
    ai_summary = {
        "mode": "rule_based_fallback",
        "summary": "AI API key not configured. The system used the rule-based sourcing evaluation with supplier data from the database only.",
        "notes": [
            "No supplier, price, certification, or stock information was invented.",
            "Only documented database entries and configured source labels were used.",
        ],
    }

    if os.getenv("OPENAI_API_KEY"):
        ai_summary = {
            "mode": "ai_assisted",
            "summary": "AI integration is configured and the request was evaluated using the structured supplier database.",
            "notes": [
                "The AI layer should be used only for summarization and risk analysis; humans must approve all external actions.",
            ],
        }

    report = {
        "buyer_requirements": {
            "buyer_name": request.buyer_name,
            "company_name": request.company_name,
            "email": request.email,
            "commodity": request.commodity,
            "grade_or_spec": request.grade_or_spec or "Unknown",
            "quantity": request.quantity or "Unknown",
            "quantity_unit": request.quantity_unit or "Unknown",
            "origin_country": request.origin_country or "Unknown",
            "destination_country": request.destination_country or "Unknown",
            "target_price": request.target_price or "Not provided",
            "currency": request.currency or "Not provided",
            "certifications_required": request.certifications_required or "Not provided",
            "delivery_timeline": request.delivery_timeline or "Not provided",
            "notes": request.notes or "Not provided",
        },
        "candidate_count": len(candidates),
        "candidates": [
            {
                "company_name": candidate["supplier"].company_name,
                "country": candidate["supplier"].country,
                "commodities_supplied": candidate["supplier"].commodities_supplied,
                "quantity_claim": candidate["supplier"].quantity_claim or "Unknown",
                "indicative_price": candidate["supplier"].indicative_price or "Unknown",
                "currency": candidate["supplier"].currency or "Not provided",
                "verification_status": candidate["supplier"].verification_status,
                "match_score": candidate["match_score"],
                "suitability": "Suitable candidate" if candidate["is_viable"] else "Needs further review",
                "reasons": candidate["reasons"],
                "source_of_information": candidate["supplier"].source_of_information,
                "information_date": candidate["supplier"].information_date or "Unknown",
                "certificates": candidate["supplier"].certificates or "Not provided",
            }
            for candidate in candidates
        ],
        "ai_summary": ai_summary,
        "disclaimer": "This report does not guarantee a transaction, supplier legitimacy, or stock availability. All findings should be reviewed by a human operator before outreach or commitment.",
        "download_text": build_report_download_text(request, candidates, ai_summary),
    }
    return report


def build_report_download_text(request: BuyerRequest, candidates: List[Dict[str, Any]], ai_summary: Dict[str, Any]) -> str:
    lines = [
        "AFRICA SOURCING AGENT - SOURCING REPORT",
        "=====================================",
        f"Buyer: {request.buyer_name} ({request.company_name})",
        f"Commodity: {request.commodity}",
        f"Grade/Spec: {request.grade_or_spec or 'Unknown'}",
        f"Quantity: {request.quantity or 'Unknown'} {request.quantity_unit or ''}",
        f"Origin: {request.origin_country}",
        f"Destination: {request.destination_country}",
        "",
        "Matching Supplier Candidates:",
    ]
    if not candidates:
        lines.append("No supplier candidates met the minimum evaluation threshold.")
    else:
        for index, candidate in enumerate(candidates, start=1):
            supplier = candidate["supplier"]
            lines.extend(
                [
                    f"{index}. {supplier.company_name}",
                    f"   Country: {supplier.country}",
                    f"   Verification status: {supplier.verification_status}",
                    f"   Match score: {candidate['match_score']}",
                    f"   Indicative price: {supplier.indicative_price or 'Unknown'} {supplier.currency or ''}",
                    f"   Source: {supplier.source_of_information}",
                    "",
                ]
            )
    lines.extend(["", "AI / Decision Summary:", ai_summary["summary"], ""])
    lines.extend(["Disclaimer:", "This report is not a guarantee of legitimacy, availability, or transaction completion."])
    return "\n".join(lines)


def prepare_outreach_email(request: BuyerRequest, supplier: Supplier) -> str:
    return (
        f"Subject: Request for quotation - {request.commodity} sourced from {supplier.country}\n\n"
        f"Hello {supplier.company_name},\n\n"
        f"We are evaluating suppliers for {request.commodity} with the following requirements: "
        f"{request.quantity or 'unknown quantity'} {request.quantity_unit or ''}, origin {request.origin_country}, "
        f"destination {request.destination_country}.\n\n"
        f"Please confirm whether you can supply the requested specification, quantity, and lead time. "
        f"If you are interested, please share the latest pricing, certifications, and supporting documents.\n\n"
        f"Important: This outreach must be approved by a human operator before any formal communication is sent.\n\n"
        f"Best regards,\n{request.buyer_name}\n{request.company_name}\n{request.email}"
    )
