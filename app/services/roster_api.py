import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

base_url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/phi/roster'

def get_eagles_roster():
    response = requests.get(base_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from the API {response.status_code}")
        return {"error": "Failed to fetch roster data"}
    
    eagles_data = response.json()
    players = []
    
    for group in eagles_data.get("athletes", []):
        group_position = group.get("position", "Unknown")  # This is "offense", "defense", "specialTeam"
        
        for player in group.get("items", []):
            # Extract basic info
            name = player.get("displayName", "N/A")
            jersey = player.get("jersey", "N/A")
            
            # Position info - this is nested differently
            position_info = player.get("position", {})
            if isinstance(position_info, dict):
                position = position_info.get("abbreviation", "N/A")
            else:
                position = "N/A"
            
            # Physical attributes
            age = player.get("age", "N/A")
            weight = player.get("displayWeight", player.get("weight", "N/A"))
            height = player.get("displayHeight", player.get("height", "N/A"))
            
            # Experience
            experience_info = player.get("experience", {})
            if isinstance(experience_info, dict):
                experience = experience_info.get("years", "N/A")
            else:
                experience = "N/A"
            
            # College info
            college_info = player.get("college", {})
            if isinstance(college_info, dict):
                college = college_info.get("name", "N/A")
            else:
                college = "N/A"
            
            # Birth place
            birth_place_data = player.get('birthPlace', {})
            if isinstance(birth_place_data, dict):
                birth_place = ', '.join(filter(None, [
                    birth_place_data.get('city'),
                    birth_place_data.get('state'),
                    birth_place_data.get('country')
                ]))
            else:
                birth_place = "N/A"
            
            player_data = {
                "name": name,
                "position": position,
                "jersey": jersey,
                "college": college,
                "birth_place": birth_place,
                "age": age,
                "weight": weight,
                "height": height,
                "experience": experience,
                "group_position": group_position  # offense, defense, specialTeam
            }
            
            players.append(player_data)
    
    return {"players": players}

if __name__ == "__main__":
    roster = get_eagles_roster()
    print(roster)