# app/services/pdf_downloader.py
import os
import requests
from pathlib import Path

def download_pdfs_if_needed():
    """Download PDFs from cloud storage if they don't exist locally"""
    
    # Create data directory if it doesn't exist
    data_dir = Path("data/sports_docs_chatbot")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # PDF URLs from AWS S3
    S3_BASE_URL = "https://eagles-backend-assets.s3.us-east-1.amazonaws.com/sports_docs_chatbot"
    
    pdf_urls = {
        "2022_NFL_Record_and_Fact_Book.pdf": f"{S3_BASE_URL}/2022_NFL_Record_and_Fact_Book.pdf",
        "2024-hall-of-fame-media-guide.pdf": f"{S3_BASE_URL}/2024-hall-of-fame-media-guide.pdf", 
        "2024-nfl-rulebook.pdf": f"{S3_BASE_URL}/2024-nfl-rulebook.pdf",
        "AB0920.pdf": f"{S3_BASE_URL}/AB0920.pdf",
        "AB0920 (1).pdf": f"{S3_BASE_URL}/AB0920%20(1).pdf",  # URL-encoded
        "Eagles, 2023 Media Guide.pdf": f"{S3_BASE_URL}/Eagles,%202023%20Media%20Guide.pdf"  # URL-encoded
    }
    
    for filename, url in pdf_urls.items():
        file_path = data_dir / filename
        
        # Skip if file already exists
        if file_path.exists():
            print(f"✅ {filename} already exists")
            continue
            
        try:
            print(f"📥 Downloading {filename}...")
            
            # S3 URLs are direct - no conversion needed
            direct_url = url
            
            # Download the file
            response = requests.get(direct_url, stream=True)
            response.raise_for_status()
            
            # Save to file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            print(f"✅ Downloaded {filename}")
            
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            
    print("🎉 PDF download check complete!")


def get_pdf_status():
    """Check which PDFs are available"""
    data_dir = Path("data/sports_docs_chatbot")
    
    if not data_dir.exists():
        return {"status": "no_pdfs", "count": 0, "files": []}
        
    pdf_files = list(data_dir.glob("*.pdf"))
    
    return {
        "status": "ready" if pdf_files else "no_pdfs",
        "count": len(pdf_files), 
        "files": [f.name for f in pdf_files]
    }