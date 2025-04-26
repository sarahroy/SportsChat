import os
from dotenv import load_dotenv
import main as sports_app
import requests
import json

# Load environment variables
load_dotenv()
# Add this line to get the API key
THESPORTSDB_API_KEY = os.getenv("THESPORTSDB_API_KEY")

def test_team_updates(team_name):
    """Test real-time updates for a specific team"""
    print(f"\n=== Testing real-time updates for {team_name} ===\n")
    
    # Get basic team info
    team_info = sports_app.get_team_info(team_name)
    if not team_info:
        print(f"Could not find team: {team_name}")
        return
    
    print(f"Team: {team_info['team']}")
    print(f"League: {team_info['league']}")
    print(f"Stadium: {team_info['stadium']}")
    print(f"Team ID: {team_info['team_id']}")
    
    # Get latest results
    results = sports_app.get_latest_results(team_info['team_id'])
    print("\n--- Latest Results ---")
    if results:
        for result in results:
            print(f"{result['date']}: {result['home_team']} {result['home_score']} - {result['away_score']} {result['away_team']}")
    else:
        print("No recent results found")
    
    # Get upcoming fixtures
    fixtures = sports_app.get_upcoming_matches(team_info['team_id'])
    print("\n--- Upcoming Fixtures ---")
    if fixtures:
        for fixture in fixtures:
            print(f"{fixture['date']} {fixture['time']}: {fixture['home_team']} vs {fixture['away_team']} at {fixture['venue']}")
    else:
        print("No upcoming fixtures found")
    
    # Get league standings
    league_id = get_league_id(team_info['team_id'])
    if league_id:
        standings = sports_app.get_league_standings(league_id)
        print(f"\n--- League Standings (ID: {league_id}) ---")
        if standings:
            for team in standings[:5]:  # Show top 5
                print(f"{team['position']}. {team['team']} - {team['points']} points ({team['played']} games)")
        else:
            print("No standings data found")
    else:
        print("Could not retrieve league ID")
    
    # Debug API calls for this team
    debug_api_responses(team_info['team_id'])

def get_league_id(team_id):
    """Get league ID from team ID with sport-specific handling"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/lookupteam.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    if data and "teams" in data and data["teams"]:
        team = data["teams"][0]
        sport = team.get("strSport", "").lower()
        
        # Map sports to their primary league IDs based on your test results
        sport_league_map = {
            "soccer": team.get("idLeague"),  # Soccer/Football uses the team's league
            "basketball": "4387",  # NBA
            "ice hockey": "4380",  # NHL
            "american football": "4391"  # NFL
        }
        
        # Return sport-specific league ID or team's league ID as fallback
        return sport_league_map.get(sport, team.get("idLeague"))
    
    return None

def get_upcoming_matches(team_id, limit=3):
    """Get the team's upcoming fixtures with fallback for limited data"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/eventsnext.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    fixtures = []
    if data and "events" in data and data["events"]:
        # Check if we're getting generic data (Bolton vs Peterboro) or actual team data
        team_name = get_team_name_from_id(team_id)
        genuine_fixtures = False
        
        for event in data["events"][:limit]:
            # Check if the event actually involves our team
            if team_name and (team_name in event["strHomeTeam"] or team_name in event["strAwayTeam"]):
                genuine_fixtures = True
            
            fixtures.append({
                "date": event["dateEvent"],
                "time": event.get("strTime", "TBD"),
                "home_team": event["strHomeTeam"],
                "away_team": event["strAwayTeam"],
                "venue": event["strVenue"],
                "league": event["strLeague"]
            })
        
        # If we determined these aren't genuine fixtures for our team
        if not genuine_fixtures:
            fixtures = []
    
    return fixtures

def get_team_name_from_id(team_id):
    """Helper function to get team name from ID"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/lookupteam.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    if data and "teams" in data and data["teams"]:
        return data["teams"][0].get("strTeam")
    return None

def debug_api_responses(team_id):
    """Debug API responses for a specific team ID"""
    api_key = os.getenv("THESPORTSDB_API_KEY")
    
    # Debug upcoming fixtures
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsnext.php?id={team_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("\n--- DEBUG: Upcoming Fixtures API Response ---")
        if "events" in data and data["events"]:
            print(f"Found {len(data['events'])} upcoming events")
        else:
            print("No upcoming events in API response")
    
    # Debug league ID
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/lookupteam.php?id={team_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("\n--- DEBUG: Team League Info ---")
        if "teams" in data and data["teams"]:
            team = data["teams"][0]
            print(f"League ID: {team.get('idLeague', 'None')}")
            print(f"League Name: {team.get('strLeague', 'None')}")
            print(f"Sport: {team.get('strSport', 'None')}")
        else:
            print("No team data in API response")

if __name__ == "__main__":
    # Test multiple teams from different leagues
    teams_to_test = [
        "Arsenal",           # EPL
        "Los Angeles Lakers", # NBA
        "Toronto Maple Leafs", # NHL
        "Kansas City Chiefs"   # NFL
    ]
    
    for team in teams_to_test:
        test_team_updates(team)
        print("\n" + "="*50 + "\n")