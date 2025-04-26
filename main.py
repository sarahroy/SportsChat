import os
import requests
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
# API Keys
THESPORTSDB_API_KEY = os.getenv("THESPORTSDB_API_KEY")

# Ollama Client with updated class
llm = OllamaLLM(model="llama3.2")  # Use the updated class

def get_team_info(team_name):
    """Fetch team details from TheSportsDB API"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/searchteams.php?t={team_name}"
    response = requests.get(url)
    data = response.json()
    
    if data["teams"]:
        team = data["teams"][0]
        return {
            "team": team["strTeam"],
            "league": team["strLeague"],
            "stadium": team["strStadium"],
            "team_id": team["idTeam"]
        }
    else:
        return None

def get_latest_results(team_id, limit=5):
    """Get the team's most recent matches"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/eventslast.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    results = []
    if data and "results" in data and data["results"]:
        for event in data["results"][:limit]:
            results.append({
                "date": event["dateEvent"],
                "home_team": event["strHomeTeam"],
                "away_team": event["strAwayTeam"],
                "home_score": event["intHomeScore"],
                "away_score": event["intAwayScore"],
                "league": event["strLeague"]
            })
    return results

def get_upcoming_matches(team_id, limit=3):
    """Get the team's upcoming fixtures"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/eventsnext.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    fixtures = []
    if data and "events" in data and data["events"]:
        for event in data["events"][:limit]:
            fixtures.append({
                "date": event["dateEvent"],
                "time": event.get("strTime", "TBD"),
                "home_team": event["strHomeTeam"],
                "away_team": event["strAwayTeam"],
                "venue": event["strVenue"],
                "league": event["strLeague"]
            })
    return fixtures

def get_league_standings(league_id):
    """Get current league standings"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/lookuptable.php?l={league_id}&s=2023-2024"
    response = requests.get(url)
    data = response.json()
    
    standings = []
    if data and "table" in data and data["table"]:
        for team in data["table"][:10]:  # Top 10 teams
            standings.append({
                "position": team["intRank"],
                "team": team["strTeam"],
                "played": team["intPlayed"],
                "points": team["intPoints"]
            })
    return standings

def get_league_id(team_id):
    """Get league ID from team ID"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/lookupteam.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    if data and "teams" in data and data["teams"]:
        return data["teams"][0].get("idLeague")
    return None

def generate_response(team_name, info_type="all"):
    """Get team info and pass it to Ollama for a conversational reply"""
    team_info = get_team_info(team_name)
    
    if not team_info:
        return "Sorry, I couldn't find that team."
    
    team_id = team_info["team_id"]
    prompt_data = {
        "team": team_info["team"],
        "league": team_info["league"],
        "stadium": team_info["stadium"]
    }
    
    if info_type in ["all", "results"]:
        results = get_latest_results(team_id)
        if results:
            prompt_data["latest_results"] = results
    
    if info_type in ["all", "fixtures"]:
        fixtures = get_upcoming_matches(team_id)
        if fixtures:
            prompt_data["upcoming_fixtures"] = fixtures
    
    if info_type in ["all", "standings"]:
        league_id = get_league_id(team_id)
        if league_id:
            standings = get_league_standings(league_id)
            if standings:
                prompt_data["standings"] = standings
    
    # Construct a detailed prompt based on available data
    prompt = f"A user asked about {prompt_data['team']} from {prompt_data['league']}. "
    prompt += f"The team plays at {prompt_data['stadium']}. "
    
    if "latest_results" in prompt_data and prompt_data["latest_results"]:
        prompt += "\nLatest results:\n"
        for result in prompt_data["latest_results"]:
            prompt += (f"- {result['date']}: {result['home_team']} {result['home_score']} - "
                     f"{result['away_score']} {result['away_team']}\n")
    
    if "upcoming_fixtures" in prompt_data and prompt_data["upcoming_fixtures"]:
        prompt += "\nUpcoming fixtures:\n"
        for fixture in prompt_data["upcoming_fixtures"]:
            prompt += f"- {fixture['date']} {fixture['time']}: {fixture['home_team']} vs {fixture['away_team']} at {fixture['venue']}\n"
    
    if "standings" in prompt_data and prompt_data["standings"]:
        prompt += "\nCurrent standings in the league:\n"
        for team in prompt_data["standings"][:5]:  # Show top 5
            prompt += f"- {team['position']}. {team['team']} - {team['points']} points ({team['played']} games)\n"
    
    prompt += "\nCreate a conversational response in a friendly sports announcer style, focusing on the most recent and upcoming events."
    
    response = llm.invoke(prompt)
    return response

if __name__ == "__main__":
    print("SportsChat - Real-time sports updates")
    print("1. Team Information")
    print("2. Latest Results")
    print("3. Upcoming Fixtures")
    print("4. League Standings")
    print("5. All Information")
    
    try:
        choice = int(input("Enter your choice (1-5): "))
        team_name = input("Enter a team name: ")
        
        info_map = {
            1: "basic",
            2: "results",
            3: "fixtures",
            4: "standings",
            5: "all"
        }
        
        info_type = info_map.get(choice, "all")
        response = generate_response(team_name, info_type)
        print("\n" + response)
    except ValueError:
        print("Please enter a valid number.")
