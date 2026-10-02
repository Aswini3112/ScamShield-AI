"""Recovery mode route."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import RecoveryRequest, ApiResponse
from app.services.recovery_service import get_recovery_guidance
from app.services.scan_service import save_recovery_session

router = APIRouter(tags=["recovery"])


@router.post("/recovery", response_model=ApiResponse)
async def submit_recovery(
    request: RecoveryRequest,
    db: AsyncSession = Depends(get_db),
):
    guidance = get_recovery_guidance(request.interaction_type)
    await save_recovery_session(db, request.scan_id, request.interaction_type)
    return ApiResponse(success=True, data=guidance.model_dump(mode="json"))
