from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import APP_NAME
from app.database import Base, engine
from app.models import BuyerRequest, Supplier  # noqa: F401 - register SQLAlchemy models


def seed_demo_data(db: Session) -> None:
    """Seed one clearly labelled fictional record when explicitly called."""
    if db.query(Supplier).count() > 0:
        return
    db.add(Supplier(
        company_name="DEMO: Nigeria Sesame Exporters",
        contact_name="Sample Contact",
        email="sample@example.com",
        country="Nigeria",
        operating_location="Kano, Nigeria",
        commodities_supplied="sesame",
        quantity_claim="500 MT (demo claim)",
        specification="Demo only: premium grade white sesame",
        indicative_price=None,
        currency="USD",
        source_of_information="DEMO DATA - fictional sample record; not a real supplier",
        information_date="",
        certificates="Not verified",
        verification_status="unverified",
        verification_notes="Fictional demonstration record. Do not contact or rely on it.",
        is_demo_data=True,
    ))
    db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Starter convenience only; use database migrations before production use.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=APP_NAME, version="0.1.0", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def homepage() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{APP_NAME}</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;font:16px/1.6 system-ui,sans-serif;background:#f5f8f6;color:#18342b}}
main{{max-width:850px;margin:8vh auto;padding:2rem}}section{{background:white;border:1px solid #dce8e1;border-radius:18px;padding:clamp(1.5rem,5vw,3rem);box-shadow:0 16px 48px #18342b12}}
small{{color:#27734e;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}h1{{font-size:clamp(2rem,5vw,3.4rem);line-height:1.1}}p{{color:#52675e}}a{{color:#216644}}
</style></head><body><main><section>
<small>Free-first project foundation</small><h1>{APP_NAME}</h1>
<p>A workspace foundation for organising buyer requirements, recording supplier evidence, and comparing sourcing candidates across African commodities.</p>
<h2>What comes next</h2><ul><li>Record buyer requests and supplier profiles.</li><li>Compare candidates using transparent, rule-based criteria.</li><li>Track evidence before supplier outreach.</li></ul>
<p><strong>Important:</strong> Sample records are fictional. Supplier identity, prices, stock, certificates, and availability must be independently verified.</p>
<p>Service status: <a href="/health">health check</a> · API docs: <a href="/docs">/docs</a></p>
</section></main></body></html>"""


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": APP_NAME}


@app.get("/api")
def api_info() -> dict[str, str]:
    return {"name": APP_NAME, "version": "0.1.0", "docs": "/docs"}
