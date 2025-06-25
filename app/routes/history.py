from fastapi import APIRouter
from pydantic import BaseModel
from app.services.history_api import get_history_prompt, get_fun_fact_prompt, get_legend_prompt, ask_openai
from app.services.chatbot_core import query_bot  # Import from your actual chatbot file

router = APIRouter()

# Pydantic model for chat messages
class ChatMessage(BaseModel):
    message: str

@router.get("/eagles-history")
def eagles_history():
    prompt = get_history_prompt()
    answer = ask_openai(prompt)
    return {"history": answer}

@router.get("/eagles-fun-fact")
def eagles_fun_fact():
    prompt = get_fun_fact_prompt()
    answer = ask_openai(prompt)
    return {"fun_fact": answer}

@router.get("/eagles-legend/{player_name}")
def eagles_legend(player_name: str):
    prompt = get_legend_prompt(player_name)
    answer = ask_openai(prompt)
    return {"legend": answer}

# Chat endpoint using your chatbot_core
@router.post("/chat")
def chat_bot_endpoint(chat_message: ChatMessage):
    response = query_bot(chat_message.message)
    return {"response": response}