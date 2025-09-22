import aiofiles
import os
from pathlib import Path
from fastapi import UploadFile
import uuid

async def save_upload_file(upload_file: UploadFile, patient_id: str) -> str:
    """Save uploaded file to disk"""
    # Create uploads directory if it doesn't exist
    upload_dir = Path("uploads") / patient_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(upload_file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)
    
    return str(file_path)

def ensure_directories():
    """Ensure required directories exist"""
    directories = ["uploads", "backend/models"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)