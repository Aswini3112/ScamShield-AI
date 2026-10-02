"""Analysis API routes — text, URL, image, QR, document."""
from __future__ import annotations

import io
import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.schemas import (
    AnalyzeTextRequest, AnalyzeUrlRequest,
    AnalysisResult, ApiResponse,
)
from app.services.analysis_service import analyze_text, analyze_url_content
from app.services.scan_service import save_scan
from app.analyzers import analyze_image_bytes, analyze_qr_bytes, extract_text_from_document, ALLOWED_MIME_TYPES

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/analyze", tags=["analysis"])

# ── helpers ───────────────────────────────────────────────────────────────────

def _validate_upload(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: {', '.join(ALLOWED_MIME_TYPES)}",
        )


async def _read_upload(file: UploadFile) -> bytes:
    data = await file.read()
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_upload_mb} MB.",
        )
    return data


# ── POST /api/analyze/text ────────────────────────────────────────────────────

@router.post("/text", response_model=ApiResponse)
async def analyze_text_endpoint(
    request: AnalyzeTextRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = analyze_text(request.text, request.language)
        scan_id = await save_scan(db, result, "text")
        result.id = scan_id
        return ApiResponse(success=True, data=result.model_dump(mode="json"))
    except Exception as e:
        logger.exception("Text analysis error")
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /api/analyze/url ─────────────────────────────────────────────────────

@router.post("/url", response_model=ApiResponse)
async def analyze_url_endpoint(
    request: AnalyzeUrlRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = analyze_url_content(request.url)
        scan_id = await save_scan(db, result, "url")
        result.id = scan_id
        return ApiResponse(success=True, data=result.model_dump(mode="json"))
    except Exception as e:
        logger.exception("URL analysis error")
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /api/analyze/image ───────────────────────────────────────────────────

@router.post("/image", response_model=ApiResponse)
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    _validate_upload(file)
    image_bytes = await _read_upload(file)

    try:
        img_result = analyze_image_bytes(image_bytes)
        ocr_text = img_result.get("ocr_text", "")

        if not ocr_text and not img_result.get("qr_detected"):
            # Return a minimal low-risk result when nothing could be extracted
            from app.schemas.analysis import Recommendation
            result = AnalysisResult(
                risk_score=5,
                risk_level="LOW",
                category="No Text Detected",
                summary="No readable text could be extracted from this image.",
                indicators=[],
                social_engineering=[],
                attack_chain=[],
                recommendations=[
                    Recommendation(type="do", text="Ensure the image is clear and contains text."),
                ],
                evidence=[],
                explanation="OCR could not extract text from this image. Install pytesseract and OpenCV for full OCR support.",
                input_type="image",
            )
        else:
            # Run full text analysis on OCR output
            text_to_analyze = ocr_text or img_result.get("qr_content", "")
            result = analyze_text(text_to_analyze)
            result.input_type = "image"
            result.extracted_text = ocr_text
            result.qr_detected = img_result.get("qr_detected", False)
            result.qr_content = img_result.get("qr_content")

        scan_id = await save_scan(db, result, "image")
        result.id = scan_id
        return ApiResponse(success=True, data=result.model_dump(mode="json"))
    except Exception as e:
        logger.exception("Image analysis error")
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /api/analyze/qr ──────────────────────────────────────────────────────

@router.post("/qr", response_model=ApiResponse)
async def analyze_qr_endpoint(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    _validate_upload(file)
    image_bytes = await _read_upload(file)

    try:
        qr_result = analyze_qr_bytes(image_bytes)
        qr_detected = qr_result.get("qr_detected", False)
        qr_content = qr_result.get("qr_content", "")

        if not qr_detected:
            from app.schemas.analysis import Recommendation
            result = AnalysisResult(
                risk_score=0,
                risk_level="LOW",
                category="No QR Detected",
                summary="No QR code was detected in the uploaded image.",
                indicators=[],
                social_engineering=[],
                attack_chain=[],
                recommendations=[
                    Recommendation(type="do", text="Ensure the QR code is clearly visible and well-lit in the image."),
                ],
                evidence=[],
                explanation="OpenCV QRCodeDetector did not find a QR code. Try a clearer image.",
                qr_detected=False,
                input_type="qr",
            )
        else:
            # Analyse the decoded QR content
            if qr_content.startswith(("http://", "https://")):
                result = analyze_url_content(qr_content)
                result.qr_detected = True
                result.qr_content = qr_content
                result.input_type = "qr"
                result.summary = f"QR code decoded. URL analysis: {result.summary}"
            else:
                result = analyze_text(qr_content)
                result.qr_detected = True
                result.qr_content = qr_content
                result.input_type = "qr"

        scan_id = await save_scan(db, result, "qr")
        result.id = scan_id
        return ApiResponse(success=True, data=result.model_dump(mode="json"))
    except Exception as e:
        logger.exception("QR analysis error")
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /api/analyze/document ────────────────────────────────────────────────

@router.post("/document", response_model=ApiResponse)
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    allowed_doc_types = {
        "application/pdf", "text/plain", "image/png", "image/jpeg",
        "image/webp", "image/gif",
    }
    if file.content_type not in allowed_doc_types:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported document type. Allowed: PDF, TXT, PNG, JPG",
        )
    doc_bytes = await _read_upload(file)

    try:
        extracted = extract_text_from_document(
            doc_bytes, file.content_type or "", file.filename or ""
        )

        if not extracted.strip():
            from app.schemas.analysis import Recommendation
            result = AnalysisResult(
                risk_score=5,
                risk_level="LOW",
                category="No Text Extracted",
                summary="Could not extract readable text from this document.",
                indicators=[],
                social_engineering=[],
                attack_chain=[],
                recommendations=[
                    Recommendation(type="do", text="Ensure the document contains readable text."),
                ],
                evidence=[],
                explanation="Text extraction yielded no content. Install PyMuPDF for PDF support.",
                input_type="document",
            )
        else:
            result = analyze_text(extracted)
            result.input_type = "document"
            result.extracted_text = extracted[:500] + "..." if len(extracted) > 500 else extracted

        scan_id = await save_scan(db, result, "document")
        result.id = scan_id
        return ApiResponse(success=True, data=result.model_dump(mode="json"))
    except Exception as e:
        logger.exception("Document analysis error")
        raise HTTPException(status_code=500, detail=str(e))
