# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.recognize import router as recognize_router
from api.register import router as register_router
from api.attendance import router as attendance_router
import os

app = FastAPI(title="FaceRoll-AI")

# Mount API routes
app.include_router(recognize_router, prefix="/api")
app.include_router(register_router, prefix="/api")
app.include_router(attendance_router, prefix="/api")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/register")
def register_page():
    return FileResponse("static/register.html")

@app.get("/attendance")
def attendance_page():
    return FileResponse("static/attendance.html")