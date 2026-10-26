from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BuyerRequest(Base):
    __tablename__ = "buyer_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    buyer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=True)
    commodity: Mapped[str] = mapped_column(String(200), nullable=False)
    grade_or_spec: Mapped[str] = mapped_column(String(200), nullable=True)
    quantity: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    origin_country: Mapped[str] = mapped_column(String(100), nullable=False)
    destination_country: Mapped[str] = mapped_column(String(100), nullable=False)
    target_price: Mapped[str] = mapped_column(String(100), nullable=True)
    currency: Mapped[str] = mapped_column(String(50), nullable=True)
    certifications_required: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_timeline: Mapped[str] = mapped_column(String(200), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_name: Mapped[str] = mapped_column(String(200), nullable=True)
    email: Mapped[str] = mapped_column(String(200), nullable=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    operating_location: Mapped[str] = mapped_column(String(200), nullable=True)
    commodities_supplied: Mapped[str] = mapped_column(Text, nullable=False)
    quantity_claim: Mapped[str] = mapped_column(String(100), nullable=True)
    specification: Mapped[str] = mapped_column(Text, nullable=True)
    indicative_price: Mapped[str] = mapped_column(String(100), nullable=True)
    currency: Mapped[str] = mapped_column(String(50), nullable=True)
    source_of_information: Mapped[str] = mapped_column(Text, nullable=False)
    information_date: Mapped[str] = mapped_column(String(100), nullable=True)
    certificates: Mapped[str] = mapped_column(Text, nullable=True)
    verification_status: Mapped[str] = mapped_column(String(50), default="unverified")
    verification_notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_demo_data: Mapped[bool] = mapped_column(default=False)
