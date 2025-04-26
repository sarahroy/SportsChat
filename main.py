import os
import requests
from dotenv import load_dotenv
# Update this import to use the new package
from langchain_ollama import OllamaLLM

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
            "stadium": team["strStadium"]
        }
    else:
        return None

def generate_response(team_name):
    """Get team info and pass it to Ollama for a conversational reply"""
    team_info = get_team_info(team_name)
    
    if team_info:
        prompt = f"""A user asked about {team_info['team']} from {team_info['league']}. 
        The team plays at {team_info['stadium']}. 
        Create a conversational response in a friendly sports announcer style."""
        
        response = llm.invoke(prompt)
        return response
    else:
        return "Sorry, I couldn't find that team."

if __name__ == "__main__":
    team_name = input("Enter a team name: ")
    response = generate_response(team_name)
    print(response)
