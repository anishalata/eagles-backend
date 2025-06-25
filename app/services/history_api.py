from fastapi import APIRouter
from openai import OpenAI
import os
from dotenv import load_dotenv
import openai

load_dotenv()
client = OpenAI()

router = APIRouter()
# sports api summary 
# Prompt templates
def get_history_prompt():
    return "Give a detailed but beginner-friendly history of the Philadelphia Eagles franchise."

def get_fun_fact_prompt():
    return "Give me a fun, lesser-known fact about the Philadelphia Eagles. Keep it concise and exciting."

def get_legend_prompt(player_name):
    return f"Write a short biography of {player_name}, focusing on their time with the Eagles."

def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for consistency
        messages=[
            {"role": "system", "content": "You are a knowledgeable NFL historian."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()