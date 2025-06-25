from fastapi import APIRouter
from app.services import sports_api
from app.services.chatbot_core import store_game_in_chroma  # Add this import

router = APIRouter()

@router.get("/recap")
def recap():
    game = sports_api.get_eagles_last_game()
    if not game:
        return {"error": "No game data available."}
    
    # Store the game data in ChromaDB so the chatbot can access it
    try:
        store_game_in_chroma(game)
        print("✅ Game stored in ChromaDB for chatbot")
    except Exception as e:
        print(f"⚠️ Failed to store game in ChromaDB: {e}")
    
    return game