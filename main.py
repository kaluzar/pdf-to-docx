import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pdf2docx import Converter
import shutil
from pathlib import Path

app = FastAPI(title="PDF to DOCX Converter API")

# Create temporary directories for uploads and downloads
UPLOAD_DIR = Path("uploads")
DOWNLOAD_DIR = Path("downloads")

UPLOAD_DIR.mkdir(exist_ok=True)
DOWNLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "PDF to DOCX Converter API. Use /convert endpoint to convert PDF files."}

@app.post("/convert")
async def convert_pdf_to_docx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    # Generate unique filenames
    pdf_id = str(uuid.uuid4())
    pdf_path = UPLOAD_DIR / f"{pdf_id}.pdf"
    docx_path = DOWNLOAD_DIR / f"{pdf_id}.docx"
    
    try:
        # Save uploaded PDF
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Convert PDF to DOCX
        cv = Converter(str(pdf_path))
        cv.convert(str(docx_path))
        cv.close()
        
        # Clean up PDF file
        os.remove(pdf_path)
        
        # Return the DOCX file
        return FileResponse(
            path=docx_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
            filename=file.filename.replace(".pdf", ".docx"),
            background=lambda: os.remove(docx_path)  # Remove file after sending
        )
    except Exception as e:
        # Clean up in case of error
        if pdf_path.exists():
            os.remove(pdf_path)
        if docx_path.exists():
            os.remove(docx_path)
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 