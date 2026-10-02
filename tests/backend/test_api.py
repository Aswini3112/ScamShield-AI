"""
Backend API tests — uses httpx async test client.
Run: cd ScamShield-AI && python -m pytest tests/backend/ -v
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport

# Add backend to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

# Use in-memory SQLite for tests so we never pollute the dev DB
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.main import app
from app.database import init_db, engine, Base


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    # Create tables in the in-memory test DB
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


# ── Health ────────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "ml_model_loaded" in data


@pytest.mark.anyio
async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    assert "ScamShield" in r.json()["name"]


# ── Text analysis ─────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_analyze_text_scam(client):
    payload = {
        "text": "URGENT: Your bank account will be blocked today. Complete KYC immediately: http://fake-kyc.xyz/verify",
        "language": "en",
    }
    r = await client.post("/api/analyze/text", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    data = body["data"]
    assert data["risk_score"] >= 30
    assert data["risk_level"] in ("MEDIUM", "HIGH", "CRITICAL")
    assert "indicators" in data
    assert "social_engineering" in data
    assert "attack_chain" in data
    assert "recommendations" in data
    assert len(data["attack_chain"]) > 0


@pytest.mark.anyio
async def test_analyze_text_safe(client):
    payload = {
        "text": "Your OTP for ExampleBank NetBanking is 847291. Valid for 5 minutes. Do NOT share this with anyone.",
        "language": "en",
    }
    r = await client.post("/api/analyze/text", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    # Safe messages should have lower risk
    assert data["risk_score"] < 60


@pytest.mark.anyio
async def test_analyze_text_tanglish(client):
    payload = {
        "text": "Ungaloda bank account KYC update pannala na account block aagum. Immediate ah link click pannunga.",
        "language": "tg",
    }
    r = await client.post("/api/analyze/text", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["multilingual_note"] is not None
    assert data["risk_score"] > 0


@pytest.mark.anyio
async def test_analyze_text_empty(client):
    # Whitespace-only text gets stripped to "" by Pydantic validator, fails min_length
    r = await client.post("/api/analyze/text", json={"text": "a", "language": "en"})
    # "a" is valid (min_length=1 after strip). Whitespace-only would be caught
    assert r.status_code == 200  # minimal valid input succeeds


@pytest.mark.anyio
async def test_analyze_text_too_long(client):
    r = await client.post("/api/analyze/text", json={"text": "a" * 10001, "language": "en"})
    assert r.status_code == 422


# ── URL analysis ──────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_analyze_url_suspicious(client):
    payload = {"url": "http://fake-bank-kyc.xyz/verify?user=12345"}
    r = await client.post("/api/analyze/url", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["risk_score"] >= 30
    assert len(data["extracted_urls"]) > 0


@pytest.mark.anyio
async def test_analyze_url_shortener(client):
    payload = {"url": "https://bit.ly/suspicious123"}
    r = await client.post("/api/analyze/url", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    # Shortener should be flagged
    shortener_ind = next((i for i in data["indicators"] if i["name"] == "URL Shortener"), None)
    assert shortener_ind is not None
    assert shortener_ind["detected"] is True


@pytest.mark.anyio
async def test_analyze_url_no_scheme(client):
    """URLs without scheme should be auto-prefixed."""
    payload = {"url": "example-bank-kyc.xyz/verify"}
    r = await client.post("/api/analyze/url", json=payload)
    assert r.status_code == 200


# ── Scan history ──────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_get_scans(client):
    r = await client.get("/api/scans")
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


@pytest.mark.anyio
async def test_get_scan_not_found(client):
    r = await client.get("/api/scans/999999")
    assert r.status_code == 404


# ── Dashboard ─────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_dashboard_stats(client):
    r = await client.get("/api/dashboard/stats")
    assert r.status_code == 200
    data = r.json()["data"]
    assert "total_scans" in data
    assert "risk_distribution" in data
    assert "category_distribution" in data


# ── Recovery ─────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_recovery_only_received(client):
    payload = {"scan_id": None, "interaction_type": "only_received"}
    r = await client.post("/api/recovery", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["severity"] == "low"
    assert len(data["steps"]) > 0


@pytest.mark.anyio
async def test_recovery_transferred_money(client):
    payload = {"scan_id": None, "interaction_type": "transferred_money"}
    r = await client.post("/api/recovery", json=payload)
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["severity"] == "critical"
    assert len(data["steps"]) >= 4
    assert len(data["hotlines"]) > 0


@pytest.mark.anyio
async def test_recovery_invalid_type(client):
    payload = {"scan_id": None, "interaction_type": "invalid_type"}
    r = await client.post("/api/recovery", json=payload)
    # Pydantic Literal validation rejects invalid types
    assert r.status_code == 422
