"""Pydantic v2 schemas for request/response validation."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


# ── Shared sub-models ─────────────────────────────────────────────────────────

class Indicator(BaseModel):
    name: str
    detected: bool
    confidence: int = Field(ge=0, le=100)
    evidence: list[str] = Field(default_factory=list)


class SocialEngineeringTechnique(BaseModel):
    technique: str
    confidence: int = Field(ge=0, le=100)
    description: str
    evidence: list[str] = Field(default_factory=list)


class AttackChainStep(BaseModel):
    step: int
    title: str
    description: str
    technique: Optional[str] = None


class Recommendation(BaseModel):
    type: Literal["do", "dont"]
    text: str


class EvidenceItem(BaseModel):
    type: str
    value: str
    risk_indicator: bool = False


# ── Analysis result ───────────────────────────────────────────────────────────

class AnalysisResult(BaseModel):
    id: Optional[int] = None
    risk_score: int = Field(ge=0, le=100)
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    category: str
    summary: str
    indicators: list[Indicator] = Field(default_factory=list)
    social_engineering: list[SocialEngineeringTechnique] = Field(default_factory=list)
    attack_chain: list[AttackChainStep] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    extracted_text: Optional[str] = None
    extracted_urls: list[str] = Field(default_factory=list)
    qr_detected: Optional[bool] = None
    qr_content: Optional[str] = None
    explanation: str = ""
    created_at: Optional[datetime] = None
    input_type: Optional[str] = None
    multilingual_note: Optional[str] = None


# ── Requests ──────────────────────────────────────────────────────────────────

class AnalyzeTextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)
    language: str = Field(default="en", max_length=10)

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()


class AnalyzeUrlRequest(BaseModel):
    url: str = Field(min_length=4, max_length=2048)

    @field_validator("url")
    @classmethod
    def validate_url_format(cls, v: str) -> str:
        v = v.strip()
        if not v.startswith(("http://", "https://", "ftp://")):
            v = "https://" + v
        return v


class RecoveryRequest(BaseModel):
    scan_id: Optional[int] = None
    interaction_type: Literal[
        "only_received",
        "clicked_link",
        "entered_credentials",
        "shared_otp",
        "transferred_money",
        "downloaded_file",
        "not_sure",
    ]


# ── Responses ─────────────────────────────────────────────────────────────────

class ApiResponse(BaseModel):
    success: bool = True
    data: Any = None
    error: Optional[str] = None


class ScanListItem(BaseModel):
    id: int
    created_at: datetime
    input_type: str
    category: str
    risk_level: str
    risk_score: int
    summary: Optional[str] = None


class RecoveryStep(BaseModel):
    priority: Literal["immediate", "soon", "monitor"]
    title: str
    description: str
    action: Optional[str] = None


class RecoveryHotline(BaseModel):
    name: str
    number: str


class RecoveryGuidance(BaseModel):
    interaction_type: str
    severity: Literal["low", "medium", "high", "critical"]
    headline: str
    steps: list[RecoveryStep]
    hotlines: list[RecoveryHotline] = Field(default_factory=list)


class DashboardStats(BaseModel):
    total_scans: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    critical_count: int
    category_distribution: dict[str, int]
    risk_distribution: dict[str, int]
    recent_threats: list[ScanListItem]
    top_techniques: list[dict[str, Any]]
