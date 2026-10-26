from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import Supplier


def seed_demo_data(db: Session) -> None:
    if db.query(Supplier).count() > 0:
        return

    demo_suppliers = [
        Supplier(
            company_name="DEMO: Nigeria Sesame Exporters",
            contact_name="Amina Bello",
            email="amina@example.com",
            phone="+2348000000000",
            country="Nigeria",
            operating_location="Kano, Nigeria",
            commodities_supplied="sesame",
            quantity_claim="500 MT",
            specification="Premium grade white sesame, moisture < 8%",
            indicative_price="890",
            currency="USD",
            source_of_information="DEMO DATA - sample supplier record supplied for onboarding only",
            information_date="2026-10-26",
            certificates="Organic certificate, SGS inspection report",
            verification_status="under_review",
            verification_notes="DEMO DATA - not a real supplier; evidence must be independently validated.",
            is_demo_data=True,
        ),
        Supplier(
            company_name="DEMO: West Africa Copper Trading",
            contact_name="Kofi Mensah",
            email="kofi@example.com",
            phone="+2338000000000",
            country="Ghana",
            operating_location="Tema, Ghana",
            commodities_supplied="copper, cobalt",
            quantity_claim="2000 MT",
            specification="Copper cathode A grade",
            indicative_price="9800",
            currency="USD",
            source_of_information="DEMO DATA - sample supplier record supplied for onboarding only",
            information_date="2026-10-26",
            certificates="Customs export permit, company registration",
            verification_status="evidence_pending",
            verification_notes="DEMO DATA - not a real supplier; evidence must be independently checked.",
            is_demo_data=True,
        ),
        Supplier(
            company_name="DEMO: Lagos Agro Minerals",
            contact_name="Danjuma Ibrahim",
            email="danjuma@example.com",
            phone="+2348000000001",
            country="Nigeria",
            operating_location="Lagos, Nigeria",
            commodities_supplied="ginger, cashew",
            quantity_claim="300 MT",
            specification="Sorted ginger, export quality",
            indicative_price="750",
            currency="USD",
            source_of_information="DEMO DATA - sample supplier record supplied for onboarding only",
            information_date="2026-10-26",
            certificates="Phytosanitary certificate",
            verification_status="verified",
            verification_notes="DEMO DATA - not a real supplier; status is demonstration only and requires human evidence review.",
            is_demo_data=True,
        ),
    ]

    db.add_all(demo_suppliers)
    db.commit()
