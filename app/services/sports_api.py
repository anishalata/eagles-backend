import requests
from datetime import datetime

# used the sportsdb api for last game of phillies data 
base_url = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t=Philadelphia%20Eagles"
def get_eagles_last_game():
    response = requests.get(base_url)
    print(response)
    if response.status_code == 200: # 200 means success
        eagles_data = response.json()
        #print(eagles_data)
    else:
        print(f"Failed to retrieve data from the API {response.status_code}")
    
    # extracting team id amongst other things so that it is in a nicer format than one big json file 
    team_id = eagles_data['teams'][0]['idTeam'] #based off the structure of the jason file when we printed it earlier
    last_game_url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}"
    last_game_response = requests.get(last_game_url)
   # print(last_game_response)

    if last_game_response.status_code == 200:
        last_game_data = last_game_response.json()


    games = last_game_data.get("results", [])
    latest_game = last_game_data["results"],[]
    
    if not latest_game:
        print("No game found .")
        return None
    

    print("ALL returned games:")
    for g in games:
        print(g["dateEvent"], g["strEvent"])



    #sorting games by date to get most recent game 
    sorted_games = sorted(
        games, 
        key = lambda g: datetime.strptime(g["dateEvent"], "%Y-%m-%d"),
        reverse=True
    )
    
    latest_game = sorted_games[0] # this is the most recent game
    event_id = latest_game["idEvent"]  # get the event ID

    details_url = f"https://www.thesportsdb.com/api/v1/json/3/lookupevent.php?id={event_id}"
    details_response = requests.get(details_url)

    if details_response.status_code == 200:
        detailed_game_data = details_response.json()
        print("🔍 Detailed event data:")
        print(detailed_game_data)
    else:
        print("❌ Failed to get detailed data", details_response.status_code)

        #just cleaning up the json data so that it is easier to read
    clean_game = {
         "event": latest_game["strEvent"],
        "date": latest_game["dateEvent"],
        "home_team": latest_game["strHomeTeam"],
        "away_team": latest_game["strAwayTeam"],
        "score": f'{latest_game["intHomeScore"]} - {latest_game["intAwayScore"]}'
        }

    return clean_game


        #print("HERE IS THE LAST GAME DATA", last_game_data["results"][0]) # this is the last game data


if __name__ == "__main__":
    print(get_eagles_last_game())