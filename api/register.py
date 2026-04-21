# api/register.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import base64
import numpy as np
import cv2
import os
from deepface import DeepFace
from deepface_recognizer import DeepFaceRecognizer
from api.recognize import recognizer  # reuse singleton

router = APIRouter()

DATASET_PATH = "dataset"

class RegisterPayload(BaseModel):
    name: str
    phone: str
    images: List[str]  # list of 5 base64 JPEG strings

def decode_frame(b64: str) -> np.ndarray:
    if "," in b64:
        b64 = b64.split(",")[1]
    raw = base64.b64decode(b64)
    arr = np.frombuffer(raw, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

@router.post("/register")
def register(payload: RegisterPayload):
    if not payload.name or not payload.phone:
        raise HTTPException(status_code=400, detail="Name and phone required")

    if len(payload.images) != 5:
        raise HTTPException(status_code=400, detail="Exactly 5 images required")

    person_id = f"{payload.name}_{payload.phone}"
    person_dir = os.path.join(DATASET_PATH, person_id)

    if os.path.exists(person_dir):
        raise HTTPException(status_code=409, detail="Person already registered")

    os.makedirs(person_dir)

    saved = 0
    for i, b64 in enumerate(payload.images):
        frame = decode_frame(b64)
        try:
            faces = DeepFace.extract_faces(
                img_path=frame,
                detector_backend="opencv",
                enforce_detection=False
            )
            face_img = faces[0]["face"]
            # DeepFace returns float 0-1, convert to uint8
            face_uint8 = (face_img * 255).astype(np.uint8)
            save_path = os.path.join(person_dir, f"img{i+1}.jpg")
            cv2.imwrite(save_path, cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR))
            saved += 1
        except Exception as e:
            # Clean up on failure
            import shutil
            shutil.rmtree(person_dir, ignore_errors=True)
            raise HTTPException(status_code=422, detail=f"Face not detected in image {i+1}: {str(e)}")

    # Reload recognizer so new face works immediately
    recognizer.load_faces()

    return {"status": "success", "message": f"Registered {payload.name} with {saved} images"}