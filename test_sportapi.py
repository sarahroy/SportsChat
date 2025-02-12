import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key from .env
API_KEY = os.getenv("THESPORTSDB_API_KEY")

# Define a test function to fetch team details
def search_team(team_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchteams.php?t={team_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["teams"]:
            team = data["teams"][0]
            print(f"Team: {team['strTeam']}")
            print(f"League: {team['strLeague']}")
            print(f"Stadium: {team['strStadium']}")
        else:
            print("No team found.")
    else:
        print("Error:", response.status_code, response.text)

# Run the test
if __name__ == "__main__":
    search_team("Arsenal")
