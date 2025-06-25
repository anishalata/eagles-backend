from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chatbot_core import query_bot, store_game_in_chroma
from app.services.sports_api import get_eagles_last_game

router = APIRouter()

# Define the request body schema
class ChatRequest(BaseModel):
    message: str

# Define the /chat POST route
@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    response = query_bot(req.message)
    return {"response": response}


@router.post("/game-chat")
def game_chat(req: ChatRequest):
    game = get_eagles_last_game()
    store_game_in_chroma(game)  # <--- NEW
    response = query_bot(req.message)
    return {"response": response}
