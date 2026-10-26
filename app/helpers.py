from __future__ import annotations

from typing import Any, Dict, List

from app.models import BuyerRequest, Supplier


def normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().lower()


def get_supplier_commodities(supplier: Supplier) -> List[str]:
    if not supplier.commodities_supplied:
        return []
    return [item.strip() for item in supplier.commodities_supplied.split(",") if item.strip()]


def build_request_summary(request: BuyerRequest) -> Dict[str, Any]:
    return {
        "buyer": request.buyer_name,
        "company": request.company_name,
        "commodity": request.commodity,
        "grade_or_spec": request.grade_or_spec or "Not provided",
        "quantity": request.quantity,
        "quantity_unit": request.quantity_unit,
        "origin_country": request.origin_country,
        "destination_country": request.destination_country,
        "target_price": request.target_price or "Not provided",
        "currency": request.currency or "Not provided",
        "certifications_required": request.certifications_required or "Not provided",
        "delivery_timeline": request.delivery_timeline or "Not provided",
        "notes": request.notes or "Not provided",
    }
