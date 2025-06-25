# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import roster, chat, fantasy, history, recap
from app.services.pdf_downloader import download_pdfs_if_needed, get_pdf_status

app = FastAPI(title="Eagles Fan Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download PDFs on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Eagles Backend...")
    download_pdfs_if_needed()
    status = get_pdf_status()
    print(f"📄 PDF Status: {status['count']} files available")

# Include routes
app.include_router(roster.router, prefix="/api")
app.include_router(chat.router, prefix="/api") 
app.include_router(fantasy.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(recap.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Eagles Fan Backend API"}

@app.get("/health")
def health_check():
    pdf_status = get_pdf_status()
    return {
        "status": "healthy",
        "pdfs": pdf_status
    }