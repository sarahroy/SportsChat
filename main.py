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

def get_team_logo(team_name, league=None):
    """Return official team logo URL based on team name and league"""
    team_name_lower = team_name.lower().strip()
    
    # Team logo database with official URLs where possible
    logo_database = {
        # Premier League
        "arsenal": "https://resources.premierleague.com/premierleague/badges/t3.svg",
        "manchester united": "https://resources.premierleague.com/premierleague/badges/t1.svg",
        "manchester city": "https://resources.premierleague.com/premierleague/badges/t43.svg",
        "liverpool": "https://resources.premierleague.com/premierleague/badges/t14.svg",
        "chelsea": "https://resources.premierleague.com/premierleague/badges/t8.svg",
        "tottenham": "https://resources.premierleague.com/premierleague/badges/t6.svg",
        "tottenham hotspur": "https://resources.premierleague.com/premierleague/badges/t6.svg",
        
        # NBA
        "los angeles lakers": "https://cdn.nba.com/logos/nba/1610616839/global/L/logo.svg",
        "boston celtics": "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
        "golden state warriors": "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg",
        "chicago bulls": "https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg",
        "miami heat": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
        
        # NHL
        "toronto maple leafs": "https://assets.nhle.com/logos/nhl/svg/TOR_light.svg",
        "montreal canadiens": "https://assets.nhle.com/logos/nhl/svg/MTL_light.svg",
        "boston bruins": "https://assets.nhle.com/logos/nhl/svg/BOS_light.svg",
        
        # NFL
        "kansas city chiefs": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/KC",
        "san francisco 49ers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/SF",
        "dallas cowboys": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/DAL",
        
        # MLB
        "new york yankees": "https://www.mlbstatic.com/team-logos/team-cap-on-light/147.svg",
        "boston red sox": "https://www.mlbstatic.com/team-logos/team-cap-on-light/111.svg",
        "los angeles dodgers": "https://www.mlbstatic.com/team-logos/team-cap-on-light/119.svg",
    }
    
    # Exact match
    if team_name_lower in logo_database:
        return logo_database[team_name_lower]
    
    # Partial match
    for team, logo in logo_database.items():
        if team_name_lower in team or team in team_name_lower:
            return logo
    
    # If no match, try constructing URLs based on team/league patterns
    if league:
        league_lower = league.lower()
        
        # Premier League pattern
        if "premier league" in league_lower:
            # Try to find team ID from Premier League website (common pattern)
            pl_teams = {
                "arsenal": "3", 
                "aston villa": "7",
                "brentford": "94",
                "brighton": "36",
                "burnley": "90",
                "chelsea": "8",
                "crystal palace": "31",
                "everton": "11",
                "fulham": "54",
                "leicester": "13",
                "liverpool": "14",
                "manchester city": "43",
                "manchester united": "1",
                "newcastle": "4",
                "nottingham forest": "17",
                "sheffield united": "49",
                "southampton": "20",
                "tottenham": "6",
                "west ham": "21",
                "wolves": "39"
            }
            
            for pl_team, team_id in pl_teams.items():
                if pl_team in team_name_lower or team_name_lower in pl_team:
                    return f"https://resources.premierleague.com/premierleague/badges/t{team_id}.svg"
    
    # If all else fails, return empty string
    return ""

def get_team_info(team_name):
    """Fetch team details from TheSportsDB API"""
    details = get_team_details(team_name)
    if details:
        return {
            "team": details["team"],
            "league": details["league"],
            "stadium": details["stadium"],
            "team_id": details["team_id"],
            "logo": details.get("logo", "")
        }
    else:
        return None

def get_team_details(team_name):
    """Fetch extended team details including logo from TheSportsDB API"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/searchteams.php?t={team_name}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("teams") and len(data["teams"]) > 0:
        team = data["teams"][0]
        team_id = team.get("idTeam", "")
        team_name = team.get("strTeam", "")
        league = team.get("strLeague", "")
        
        # First try to get logo from TheSportsDB API
        logo_url = team.get("strTeamBadge", "")
        
        # If no logo found, try another field
        if not logo_url:
            logo_url = team.get("strTeamLogo", "")
            
        # If still no logo, try strTeamJersey as some teams have this
        if not logo_url:
            logo_url = team.get("strTeamJersey", "")
            
        # If API doesn't provide a logo, fall back to our custom database
        if not logo_url:
            logo_url = get_team_logo(team_name, league)
        
        # If we still don't have a logo, try dynamic logo generation
        if not logo_url:
            logo_url = generate_team_logo_url(team_name, league, team_id)
        
        return {
            "team": team_name,
            "league": league,
            "stadium": team.get("strStadium", "Unknown Stadium"),
            "team_id": team_id,
            "logo": logo_url,
            "banner": team.get("strTeamBanner", ""),
            "description": team.get("strDescriptionEN", "")
        }
    else:
        return None

def generate_team_logo_url(team_name, league, team_id):
    """Generate potential logo URLs based on team name and league patterns"""
    logo_urls = []
    
    # Clean team name for URL construction
    team_name_clean = team_name.lower().replace(" ", "-")
    team_name_underscore = team_name.lower().replace(" ", "_")
    team_name_simple = ''.join(c for c in team_name.lower() if c.isalnum())
    
    # League-specific patterns
    league_lower = league.lower() if league else ""
    
    # Add various possible URLs based on common patterns
    
    # TheSportsDB formats
    logo_urls.extend([
        f"https://www.thesportsdb.com/images/media/team/badge/{team_id}.png",
        f"https://www.thesportsdb.com/images/media/team/logo/{team_name_underscore}.png",
        f"https://www.thesportsdb.com/images/media/team/badge/{team_name_simple}.png"
    ])
    
    # League-specific patterns
    if "premier league" in league_lower or "football" in league_lower or "soccer" in league_lower:
        logo_urls.extend([
            f"https://resources.premierleague.com/premierleague/badges/t{team_id}.svg",
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/{team_name_clean}.png",
            f"https://images.fotmob.com/image_resources/logo/teamlogo/{team_name_clean}.png"
        ])
    
    elif "nba" in league_lower or "basketball" in league_lower:
        logo_urls.extend([
            f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg",
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{team_name_clean}.png"
        ])
    
    elif "nfl" in league_lower or "football" in league_lower:
        logo_urls.extend([
            f"https://static.www.nfl.com/image/private/f_auto/league/api/clubs/logos/{team_name_simple.upper()[:3]}",
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{team_name_clean}.png"
        ])
    
    elif "nhl" in league_lower or "hockey" in league_lower:
        logo_urls.extend([
            f"https://www.nhl.com/{team_name_clean}/prod/images/logos/logo.svg",
            f"https://assets.nhle.com/logos/nhl/svg/{team_name_simple.upper()[:3]}_light.svg",
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nhl/500/{team_name_clean}.png"
        ])
    
    # Generic ESPN pattern as fallback
    logo_urls.append(f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/teams/500/{team_name_clean}.png")
    
    # Try each URL to see if it works
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in logo_urls:
        try:
            response = requests.head(url, timeout=1, headers=headers)
            if response.status_code == 200:
                # Found a working URL
                return url
        except:
            # If there's an error, just continue to the next URL
            continue
    
    # If no URL works, return empty string
    return ""

def get_latest_results(team_id, limit=5):
    """Get the team's most recent matches with validation"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/eventslast.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    results = []
    
    # Get team name for validation
    team_name = get_team_name_from_id(team_id)
    
    if data and "results" in data and data["results"]:
        valid_results_count = 0
        
        for event in data["results"]:
            # Skip irrelevant results
            if team_name:
                if team_name.lower() not in event["strHomeTeam"].lower() and team_name.lower() not in event["strAwayTeam"].lower():
                    continue
            
            results.append({
                "date": event["dateEvent"],
                "home_team": event["strHomeTeam"],
                "away_team": event["strAwayTeam"],
                "home_score": event["intHomeScore"],
                "away_score": event["intAwayScore"],
                "league": event["strLeague"]
            })
            
            valid_results_count += 1
            if valid_results_count >= limit:
                break
    
    return results

def get_upcoming_matches(team_id, limit=3):
    """Get the team's upcoming fixtures with validation to ensure relevance"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/eventsnext.php?id={team_id}"
    response = requests.get(url)
    data = response.json()
    
    fixtures = []
    
    # First get the team name to validate fixtures
    team_name = get_team_name_from_id(team_id)
    
    if data and "events" in data and data["events"]:
        valid_fixtures_count = 0
        
        for event in data["events"]:
            # Skip irrelevant fixtures by checking if our team is actually involved
            if team_name:
                if team_name.lower() not in event["strHomeTeam"].lower() and team_name.lower() not in event["strAwayTeam"].lower():
                    continue
            
            fixtures.append({
                "date": event["dateEvent"],
                "time": event.get("strTime", "TBD"),
                "home_team": event["strHomeTeam"],
                "away_team": event["strAwayTeam"],
                "venue": event["strVenue"],
                "league": event["strLeague"]
            })
            
            valid_fixtures_count += 1
            if valid_fixtures_count >= limit:
                break
    
    return fixtures

def get_team_name_from_id(team_id):
    """Helper function to get team name from ID"""
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/lookupteam.php?id={team_id}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data and "teams" in data and data["teams"]:
            return data["teams"][0].get("strTeam")
    except:
        pass
    
    return None

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
    
    # Check if we have real data for this team
    has_real_data = False
    
    if info_type in ["all", "results"]:
        results = get_latest_results(team_id)
        if results:
            prompt_data["latest_results"] = results
            has_real_data = True
    
    if info_type in ["all", "fixtures"]:
        fixtures = get_upcoming_matches(team_id)
        if fixtures:
            prompt_data["upcoming_fixtures"] = fixtures
            has_real_data = True
    
    if info_type in ["all", "standings"]:
        league_id = get_league_id(team_id)
        if league_id:
            standings = get_league_standings(league_id)
            if standings:
                prompt_data["standings"] = standings
                has_real_data = True
    
    # Construct a detailed prompt based on available data
    prompt = f"A user asked about {prompt_data['team']} from {prompt_data['league']}. "
    prompt += f"The team plays at {prompt_data['stadium']}. "
    
    if "latest_results" in prompt_data and prompt_data["latest_results"]:
        prompt += "\nLatest results:\n"
        for result in prompt_data["latest_results"]:
            prompt += (f"- {result['date']}: {result['home_team']} {result['home_score']} - "
                     f"{result['away_score']} {result['away_team']}\n")
    else:
        prompt += "\nNo recent match results available for this team.\n"
    
    if "upcoming_fixtures" in prompt_data and prompt_data["upcoming_fixtures"]:
        prompt += "\nUpcoming fixtures:\n"
        for fixture in prompt_data["upcoming_fixtures"]:
            prompt += f"- {fixture['date']} {fixture['time']}: {fixture['home_team']} vs {fixture['away_team']} at {fixture['venue']}\n"
    else:
        prompt += "\nNo upcoming fixtures available for this team.\n"
    
    if "standings" in prompt_data and prompt_data["standings"]:
        prompt += "\nCurrent standings in the league:\n"
        for team in prompt_data["standings"][:5]:  # Show top 5
            prompt += f"- {team['position']}. {team['team']} - {team['points']} points ({team['played']} games)\n"
    else:
        prompt += "\nLeague standings are not available at this time.\n"
    
    if not has_real_data:
        prompt += "\nNote that there appears to be limited real-time data available for this team. Provide general information about the team and acknowledge the limited data availability."
    
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
