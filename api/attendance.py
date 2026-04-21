# api/attendance.py
from fastapi import APIRouter
import csv
import os

router = APIRouter()

ATTENDANCE_FILE = "attendance.csv"

@router.get("/attendance")
def get_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return {"records": []}

    records = []
    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    return {"records": records}