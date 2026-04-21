# api/recognize.py
from fastapi import APIRouter
from pydantic import BaseModel
import base64
import numpy as np
import cv2
from deepface_recognizer import DeepFaceRecognizer
from liveness import LivenessDetector
from attendance import AttendanceLogger

router = APIRouter()

# Singletons — loaded once at startup
recognizer = DeepFaceRecognizer()
liveness = LivenessDetector()
attendance_logger = AttendanceLogger()

class FramePayload(BaseModel):
    image: str  # base64 JPEG

def decode_frame(b64: str) -> np.ndarray:
    """Decode base64 JPEG string to OpenCV BGR frame."""
    # Strip data URL prefix if present: "data:image/jpeg;base64,..."
    if "," in b64:
        b64 = b64.split(",")[1]
    raw = base64.b64decode(b64)
    arr = np.frombuffer(raw, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return frame

@router.post("/recognize")
def recognize(payload: FramePayload):
    frame = decode_frame(payload.image)

    is_live = liveness.check_liveness(frame)

    if not is_live:
        return {"status": "not_live", "name": None, "message": "Move your face to confirm liveness"}

    small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    name = recognizer.recognize(small)

    if name != "Unknown":
        attendance_logger.log(name)
        return {"status": "recognized", "name": name, "message": f"Welcome, {name}!"}

    return {"status": "unknown", "name": None, "message": "Face not recognized"}