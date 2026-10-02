"""Scan history and dashboard routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ApiResponse
from app.services.scan_service import get_scan_by_id, list_scans, get_dashboard_stats

router = APIRouter(tags=["scans"])


@router.get("/scans", response_model=ApiResponse)
async def get_scans(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    items = await list_scans(db, skip=skip, limit=limit)
    return ApiResponse(success=True, data=[i.model_dump(mode="json") for i in items])


@router.get("/scans/{scan_id}", response_model=ApiResponse)
async def get_scan(scan_id: int, db: AsyncSession = Depends(get_db)):
    result = await get_scan_by_id(db, scan_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return ApiResponse(success=True, data=result.model_dump(mode="json"))


@router.get("/dashboard/stats", response_model=ApiResponse)
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    stats = await get_dashboard_stats(db)
    return ApiResponse(success=True, data=stats.model_dump(mode="json"))
