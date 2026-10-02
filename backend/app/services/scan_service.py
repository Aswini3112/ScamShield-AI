"""Database persistence for scan results and dashboard stats."""
from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import Scan, Evidence, RecoverySession
from app.schemas.analysis import AnalysisResult, ScanListItem, DashboardStats


async def save_scan(db: AsyncSession, result: AnalysisResult, input_type: str) -> int:
    """Persist an analysis result and return the scan id."""
    scan = Scan(
        input_type=input_type,
        raw_text=result.extracted_text,
        extracted_text=result.extracted_text,
        risk_score=result.risk_score,
        risk_level=result.risk_level,
        category=result.category,
        summary=result.summary,
    )
    scan.set_analysis(result.model_dump(mode="json"))

    db.add(scan)
    await db.flush()  # get the id

    # Persist evidence items
    for ev in result.evidence[:20]:
        db.add(Evidence(
            scan_id=scan.id,
            type=ev.type,
            value=ev.value[:500],
            risk_indicator=ev.risk_indicator,
        ))

    await db.commit()
    await db.refresh(scan)
    return scan.id


async def get_scan_by_id(db: AsyncSession, scan_id: int) -> AnalysisResult | None:
    result = await db.get(Scan, scan_id)
    if result is None:
        return None
    data = result.get_analysis()
    data["id"] = result.id
    data["created_at"] = result.created_at
    return AnalysisResult.model_validate(data)


async def list_scans(db: AsyncSession, skip: int = 0, limit: int = 50) -> list[ScanListItem]:
    stmt = select(Scan).order_by(Scan.created_at.desc()).offset(skip).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return [
        ScanListItem(
            id=r.id,
            created_at=r.created_at,
            input_type=r.input_type,
            category=r.category,
            risk_level=r.risk_level,
            risk_score=int(r.risk_score),
            summary=r.summary,
        )
        for r in rows
    ]


async def get_dashboard_stats(db: AsyncSession) -> DashboardStats:
    # Total
    total = (await db.execute(select(func.count(Scan.id)))).scalar_one()

    # By risk level
    risk_counts = {row[0]: row[1] for row in
                   (await db.execute(select(Scan.risk_level, func.count(Scan.id)).group_by(Scan.risk_level))).all()}

    # By category
    cat_counts = {row[0]: row[1] for row in
                  (await db.execute(select(Scan.category, func.count(Scan.id)).group_by(Scan.category))).all()}

    # Recent threats (HIGH/CRITICAL)
    recent_stmt = (
        select(Scan)
        .where(Scan.risk_level.in_(["HIGH", "CRITICAL"]))
        .order_by(Scan.created_at.desc())
        .limit(10)
    )
    recent = (await db.execute(recent_stmt)).scalars().all()
    recent_items = [
        ScanListItem(
            id=r.id,
            created_at=r.created_at,
            input_type=r.input_type,
            category=r.category,
            risk_level=r.risk_level,
            risk_score=int(r.risk_score),
            summary=r.summary,
        )
        for r in recent
    ]

    # Top social engineering techniques from stored analysis JSON
    tech_counts: dict[str, int] = {}
    sample_stmt = select(Scan.analysis_json).order_by(Scan.created_at.desc()).limit(100)
    rows = (await db.execute(sample_stmt)).scalars().all()
    for row in rows:
        if row:
            try:
                data = json.loads(row)
                for t in data.get("social_engineering", []):
                    name = t.get("technique", "")
                    if name:
                        tech_counts[name] = tech_counts.get(name, 0) + 1
            except Exception:
                pass

    top_techniques = [
        {"technique": k, "count": v}
        for k, v in sorted(tech_counts.items(), key=lambda x: -x[1])[:8]
    ]

    return DashboardStats(
        total_scans=total,
        critical_count=risk_counts.get("CRITICAL", 0),
        high_risk_count=risk_counts.get("HIGH", 0),
        medium_risk_count=risk_counts.get("MEDIUM", 0),
        low_risk_count=risk_counts.get("LOW", 0),
        category_distribution=cat_counts,
        risk_distribution=risk_counts,
        recent_threats=recent_items,
        top_techniques=top_techniques,
    )


async def save_recovery_session(
    db: AsyncSession, scan_id: int | None, interaction_type: str
) -> int:
    rec = RecoverySession(scan_id=scan_id, interaction_type=interaction_type)
    db.add(rec)
    await db.commit()
    await db.refresh(rec)
    return rec.id
