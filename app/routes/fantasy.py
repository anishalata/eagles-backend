from fastapi import APIRouter
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.services.sports_api import get_eagles_last_game


load_dotenv()
client = OpenAI()

router = APIRouter()
# sports api summary 

@router.get("/gpt-summary")
def gpt_summary():
    game = get_eagles_last_game()  # calling the function from the sports_api file
    if not game:
        raise ValueError("No game data available.")
    try:
        
        prompt = f"On {game['date']}, the game {game['event']} ended with a score of {game['score']}. Summarize this game in 3 sentences."
        print("Prompt sent to GPT:", prompt)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"summary": response.choices[0].message.content.strip()}
    
    except Exception as e:
        return {"error": str(e)}
