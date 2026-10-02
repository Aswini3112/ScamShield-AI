"""
Image / Screenshot analyzer.
Uses OpenCV + pytesseract for OCR.
Gracefully degrades if these libraries aren't installed.
"""
from __future__ import annotations

import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _try_ocr(image_bytes: bytes) -> str:
    """Attempt OCR using pytesseract. Returns empty string on failure."""
    try:
        import cv2
        import numpy as np
        import pytesseract

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return ""

        # Pre-process for better OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Threshold to improve text contrast
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        text = pytesseract.image_to_string(thresh, config="--psm 6")
        return text.strip()
    except ImportError:
        logger.warning("pytesseract/opencv not available — OCR skipped.")
        return ""
    except Exception as e:
        logger.warning("OCR failed: %s", e)
        return ""


def _try_qr_detect(image_bytes: bytes) -> tuple[bool, str]:
    """Attempt QR detection. Returns (detected, content)."""
    try:
        import cv2
        import numpy as np

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return False, ""

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            return True, data
        return False, ""
    except ImportError:
        return False, ""
    except Exception as e:
        logger.warning("QR detection failed: %s", e)
        return False, ""


def analyze_image_bytes(image_bytes: bytes) -> dict:
    """
    Returns:
      ocr_text     : extracted text
      qr_detected  : bool
      qr_content   : decoded QR string or ""
      method       : "ocr+qr" | "qr_only" | "fallback"
    """
    ocr_text = _try_ocr(image_bytes)
    qr_detected, qr_content = _try_qr_detect(image_bytes)

    method = "fallback"
    if ocr_text or qr_detected:
        method = "ocr+qr" if ocr_text else "qr_only"

    return {
        "ocr_text": ocr_text,
        "qr_detected": qr_detected,
        "qr_content": qr_content,
        "method": method,
    }


def analyze_qr_bytes(image_bytes: bytes) -> dict:
    """QR-focused analysis."""
    qr_detected, qr_content = _try_qr_detect(image_bytes)
    ocr_text = _try_ocr(image_bytes) if not qr_detected else ""

    return {
        "qr_detected": qr_detected,
        "qr_content": qr_content,
        "ocr_text": ocr_text,
    }
