from app.routes.analyze import router as analyze_router
from app.routes.scans import router as scans_router
from app.routes.recovery import router as recovery_router

__all__ = ["analyze_router", "scans_router", "recovery_router"]
