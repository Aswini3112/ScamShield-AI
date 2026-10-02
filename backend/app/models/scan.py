"""ORM models for scans, evidence, and recovery sessions."""
from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import Integer, String, Float, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    input_type: Mapped[str] = mapped_column(String(20))        # text | url | image | qr | document
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(10), default="LOW")  # LOW|MEDIUM|HIGH|CRITICAL
    category: Mapped[str] = mapped_column(String(100), default="Unknown")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    analysis_json: Mapped[str | None] = mapped_column(Text, nullable=True)  # full result as JSON

    evidence: Mapped[list[Evidence]] = relationship("Evidence", back_populates="scan", cascade="all, delete-orphan")
    recovery_sessions: Mapped[list[RecoverySession]] = relationship("RecoverySession", back_populates="scan", cascade="all, delete-orphan")

    def set_analysis(self, data: dict) -> None:
        self.analysis_json = json.dumps(data)

    def get_analysis(self) -> dict:
        if self.analysis_json:
            return json.loads(self.analysis_json)
        return {}


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("scans.id"))
    type: Mapped[str] = mapped_column(String(50))       # url | phone | keyword | qr | file
    value: Mapped[str] = mapped_column(Text)
    risk_indicator: Mapped[bool] = mapped_column(Boolean, default=False)

    scan: Mapped[Scan] = relationship("Scan", back_populates="evidence")


class RecoverySession(Base):
    __tablename__ = "recovery_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("scans.id"), nullable=True)
    interaction_type: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    scan: Mapped[Scan | None] = relationship("Scan", back_populates="recovery_sessions")
