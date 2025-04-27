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
        # Premier League (all 20 teams)
        "arsenal": "https://resources.premierleague.com/premierleague/badges/t3.svg",
        "aston villa": "https://resources.premierleague.com/premierleague/badges/t7.svg",
        "bournemouth": "https://resources.premierleague.com/premierleague/badges/t91.svg",
        "brentford": "https://resources.premierleague.com/premierleague/badges/t94.svg",
        "brighton": "https://resources.premierleague.com/premierleague/badges/t36.svg",
        "burnley": "https://resources.premierleague.com/premierleague/badges/t90.svg",
        "chelsea": "https://resources.premierleague.com/premierleague/badges/t8.svg",
        "crystal palace": "https://resources.premierleague.com/premierleague/badges/t31.svg",
        "everton": "https://resources.premierleague.com/premierleague/badges/t11.svg",
        "fulham": "https://resources.premierleague.com/premierleague/badges/t54.svg",
        "ipswich": "https://resources.premierleague.com/premierleague/badges/t52.svg",
        "leicester": "https://resources.premierleague.com/premierleague/badges/t13.svg",
        "liverpool": "https://resources.premierleague.com/premierleague/badges/t14.svg",
        "luton": "https://resources.premierleague.com/premierleague/badges/t102.svg",
        "manchester city": "https://resources.premierleague.com/premierleague/badges/t43.svg",
        "manchester united": "https://resources.premierleague.com/premierleague/badges/t1.svg",
        "newcastle": "https://resources.premierleague.com/premierleague/badges/t4.svg",
        "newcastle united": "https://resources.premierleague.com/premierleague/badges/t4.svg",
        "nottingham forest": "https://resources.premierleague.com/premierleague/badges/t17.svg",
        "sheffield united": "https://resources.premierleague.com/premierleague/badges/t49.svg",
        "southampton": "https://resources.premierleague.com/premierleague/badges/t20.svg",
        "tottenham": "https://resources.premierleague.com/premierleague/badges/t6.svg",
        "tottenham hotspur": "https://resources.premierleague.com/premierleague/badges/t6.svg",
        "west ham": "https://resources.premierleague.com/premierleague/badges/t21.svg",
        "west ham united": "https://resources.premierleague.com/premierleague/badges/t21.svg",
        "wolves": "https://resources.premierleague.com/premierleague/badges/t39.svg",
        "wolverhampton": "https://resources.premierleague.com/premierleague/badges/t39.svg",
        "wolverhampton wanderers": "https://resources.premierleague.com/premierleague/badges/t39.svg",
        
        # NBA (all 30 teams)
        "atlanta hawks": "https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg",
        "boston celtics": "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
        "brooklyn nets": "https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg",
        "charlotte hornets": "https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg",
        "chicago bulls": "https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg",
        "cleveland cavaliers": "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        "dallas mavericks": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
        "denver nuggets": "https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg",
        "detroit pistons": "https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg",
        "golden state warriors": "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg",
        "houston rockets": "https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg",
        "indiana pacers": "https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg",
        "la clippers": "https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg",
        "los angeles clippers": "https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg",
        "los angeles lakers": "https://cdn.nba.com/logos/nba/1610616839/global/L/logo.svg",
        "memphis grizzlies": "https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg",
        "miami heat": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
        "milwaukee bucks": "https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg",
        "minnesota timberwolves": "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg",
        "new orleans pelicans": "https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg",
        "new york knicks": "https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg",
        "oklahoma city thunder": "https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg",
        "orlando magic": "https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg",
        "philadelphia 76ers": "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg",
        "phoenix suns": "https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg",
        "portland trail blazers": "https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg",
        "sacramento kings": "https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg",
        "san antonio spurs": "https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg",
        "toronto raptors": "https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg",
        "utah jazz": "https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg",
        "washington wizards": "https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg",
        
        # NFL (all 32 teams)
        "arizona cardinals": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/ARI",
        "atlanta falcons": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/ATL",
        "baltimore ravens": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BAL",
        "buffalo bills": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/BUF",
        "carolina panthers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/CAR",
        "chicago bears": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/CHI",
        "cincinnati bengals": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/CIN",
        "cleveland browns": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/CLE",
        "dallas cowboys": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/DAL",
        "denver broncos": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/DEN",
        "detroit lions": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/DET",
        "green bay packers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/GB",
        "houston texans": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/HOU",
        "indianapolis colts": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/IND",
        "jacksonville jaguars": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/JAX",
        "kansas city chiefs": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/KC",
        "las vegas raiders": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/LV",
        "los angeles chargers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/LAC",
        "los angeles rams": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/LA",
        "miami dolphins": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/MIA",
        "minnesota vikings": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/MIN",
        "new england patriots": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/NE",
        "new orleans saints": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/NO",
        "new york giants": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/NYG",
        "new york jets": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/NYJ",
        "philadelphia eagles": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/PHI",
        "pittsburgh steelers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/PIT",
        "san francisco 49ers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/SF",
        "seattle seahawks": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/SEA",
        "tampa bay buccaneers": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/TB",
        "tennessee titans": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/TEN",
        "washington commanders": "https://static.www.nfl.com/t_q-best/league/api/clubs/logos/WAS",
        
        # MLB (all 30 teams)
        "arizona diamondbacks": "https://www.mlbstatic.com/team-logos/team-cap-on-light/109.svg",
        "atlanta braves": "https://www.mlbstatic.com/team-logos/team-cap-on-light/144.svg",
        "baltimore orioles": "https://www.mlbstatic.com/team-logos/team-cap-on-light/110.svg",
        "boston red sox": "https://www.mlbstatic.com/team-logos/team-cap-on-light/111.svg",
        "chicago cubs": "https://www.mlbstatic.com/team-logos/team-cap-on-light/112.svg",
        "chicago white sox": "https://www.mlbstatic.com/team-logos/team-cap-on-light/145.svg",
        "cincinnati reds": "https://www.mlbstatic.com/team-logos/team-cap-on-light/113.svg",
        "cleveland guardians": "https://www.mlbstatic.com/team-logos/team-cap-on-light/114.svg",
        "colorado rockies": "https://www.mlbstatic.com/team-logos/team-cap-on-light/115.svg",
        "detroit tigers": "https://www.mlbstatic.com/team-logos/team-cap-on-light/116.svg",
        "houston astros": "https://www.mlbstatic.com/team-logos/team-cap-on-light/117.svg",
        "kansas city royals": "https://www.mlbstatic.com/team-logos/team-cap-on-light/118.svg",
        "los angeles angels": "https://www.mlbstatic.com/team-logos/team-cap-on-light/108.svg",
        "los angeles dodgers": "https://www.mlbstatic.com/team-logos/team-cap-on-light/119.svg",
        "miami marlins": "https://www.mlbstatic.com/team-logos/team-cap-on-light/146.svg",
        "milwaukee brewers": "https://www.mlbstatic.com/team-logos/team-cap-on-light/158.svg",
        "minnesota twins": "https://www.mlbstatic.com/team-logos/team-cap-on-light/142.svg",
        "new york mets": "https://www.mlbstatic.com/team-logos/team-cap-on-light/121.svg",
        "new york yankees": "https://www.mlbstatic.com/team-logos/team-cap-on-light/147.svg",
        "oakland athletics": "https://www.mlbstatic.com/team-logos/team-cap-on-light/133.svg",
        "philadelphia phillies": "https://www.mlbstatic.com/team-logos/team-cap-on-light/143.svg",
        "pittsburgh pirates": "https://www.mlbstatic.com/team-logos/team-cap-on-light/134.svg",
        "san diego padres": "https://www.mlbstatic.com/team-logos/team-cap-on-light/135.svg",
        "san francisco giants": "https://www.mlbstatic.com/team-logos/team-cap-on-light/137.svg",
        "seattle mariners": "https://www.mlbstatic.com/team-logos/team-cap-on-light/136.svg",
        "st. louis cardinals": "https://www.mlbstatic.com/team-logos/team-cap-on-light/138.svg",
        "tampa bay rays": "https://www.mlbstatic.com/team-logos/team-cap-on-light/139.svg",
        "texas rangers": "https://www.mlbstatic.com/team-logos/team-cap-on-light/140.svg",
        "toronto blue jays": "https://www.mlbstatic.com/team-logos/team-cap-on-light/141.svg",
        "washington nationals": "https://www.mlbstatic.com/team-logos/team-cap-on-light/120.svg",
        
        # NHL (all 32 teams)
        "anaheim ducks": "https://assets.nhle.com/logos/nhl/svg/ANA_light.svg",
        "arizona coyotes": "https://assets.nhle.com/logos/nhl/svg/ARI_light.svg",
        "boston bruins": "https://assets.nhle.com/logos/nhl/svg/BOS_light.svg",
        "buffalo sabres": "https://assets.nhle.com/logos/nhl/svg/BUF_light.svg",
        "calgary flames": "https://assets.nhle.com/logos/nhl/svg/CGY_light.svg",
        "carolina hurricanes": "https://assets.nhle.com/logos/nhl/svg/CAR_light.svg",
        "chicago blackhawks": "https://assets.nhle.com/logos/nhl/svg/CHI_light.svg",
        "colorado avalanche": "https://assets.nhle.com/logos/nhl/svg/COL_light.svg",
        "columbus blue jackets": "https://assets.nhle.com/logos/nhl/svg/CBJ_light.svg",
        "dallas stars": "https://assets.nhle.com/logos/nhl/svg/DAL_light.svg",
        "detroit red wings": "https://assets.nhle.com/logos/nhl/svg/DET_light.svg",
        "edmonton oilers": "https://assets.nhle.com/logos/nhl/svg/EDM_light.svg",
        "florida panthers": "https://assets.nhle.com/logos/nhl/svg/FLA_light.svg",
        "los angeles kings": "https://assets.nhle.com/logos/nhl/svg/LAK_light.svg",
        "minnesota wild": "https://assets.nhle.com/logos/nhl/svg/MIN_light.svg",
        "montreal canadiens": "https://assets.nhle.com/logos/nhl/svg/MTL_light.svg",
        "nashville predators": "https://assets.nhle.com/logos/nhl/svg/NSH_light.svg",
        "new jersey devils": "https://assets.nhle.com/logos/nhl/svg/NJD_light.svg",
        "new york islanders": "https://assets.nhle.com/logos/nhl/svg/NYI_light.svg",
        "new york rangers": "https://assets.nhle.com/logos/nhl/svg/NYR_light.svg",
        "ottawa senators": "https://assets.nhle.com/logos/nhl/svg/OTT_light.svg",
        "philadelphia flyers": "https://assets.nhle.com/logos/nhl/svg/PHI_light.svg",
        "pittsburgh penguins": "https://assets.nhle.com/logos/nhl/svg/PIT_light.svg",
        "san jose sharks": "https://assets.nhle.com/logos/nhl/svg/SJS_light.svg",
        "seattle kraken": "https://assets.nhle.com/logos/nhl/svg/SEA_light.svg",
        "st. louis blues": "https://assets.nhle.com/logos/nhl/svg/STL_light.svg",
        "tampa bay lightning": "https://assets.nhle.com/logos/nhl/svg/TBL_light.svg",
        "toronto maple leafs": "https://assets.nhle.com/logos/nhl/svg/TOR_light.svg",
        "utah hockey club": "https://assets.nhle.com/logos/nhl/svg/UTAH_light.svg",
        "vancouver canucks": "https://assets.nhle.com/logos/nhl/svg/VAN_light.svg",
        "vegas golden knights": "https://assets.nhle.com/logos/nhl/svg/VGK_light.svg",
        "washington capitals": "https://assets.nhle.com/logos/nhl/svg/WSH_light.svg",
        "winnipeg jets": "https://assets.nhle.com/logos/nhl/svg/WPG_light.svg"
    }
    
    # Common abbreviations and alternative names for teams
    special_cases = {
        # MLB
        "diamondbacks": "arizona diamondbacks",
        "d-backs": "arizona diamondbacks",
        "sox": "boston red sox",  # Default to Red Sox, but this is ambiguous
        "white sox": "chicago white sox",
        "red sox": "boston red sox",
        "guardians": "cleveland guardians",
        "rockies": "colorado rockies",
        "tigers": "detroit tigers",
        "astros": "houston astros",
        "royals": "kansas city royals",
        "angels": "los angeles angels",
        "dodgers": "los angeles dodgers",
        "marlins": "miami marlins",
        "brewers": "milwaukee brewers",
        "twins": "minnesota twins",
        "mets": "new york mets",
        "yankees": "new york yankees",
        "athletics": "oakland athletics",
        "phillies": "philadelphia phillies",
        "pirates": "pittsburgh pirates",
        "padres": "san diego padres",
        "giants": "san francisco giants",
        "mariners": "seattle mariners",
        "cardinals": "st. louis cardinals",
        "rays": "tampa bay rays",
        "rangers": "texas rangers",
        "blue jays": "toronto blue jays",
        "nationals": "washington nationals",
        
        # NFL
        "cardinals": "arizona cardinals",
        "falcons": "atlanta falcons",
        "ravens": "baltimore ravens",
        "bills": "buffalo bills",
        "panthers": "carolina panthers",
        "bears": "chicago bears",
        "bengals": "cincinnati bengals",
        "browns": "cleveland browns",
        "cowboys": "dallas cowboys",
        "broncos": "denver broncos",
        "lions": "detroit lions",
        "packers": "green bay packers",
        "texans": "houston texans",
        "colts": "indianapolis colts",
        "jaguars": "jacksonville jaguars",
        "chiefs": "kansas city chiefs",
        "raiders": "las vegas raiders",
        "chargers": "los angeles chargers",
        "rams": "los angeles rams",
        "dolphins": "miami dolphins",
        "vikings": "minnesota vikings",
        "patriots": "new england patriots",
        "saints": "new orleans saints",
        "giants": "new york giants",
        "jets": "new york jets",
        "eagles": "philadelphia eagles",
        "philly": "philadelphia eagles",
        "steelers": "pittsburgh steelers",
        "niners": "san francisco 49ers",
        "49ers": "san francisco 49ers",
        "seahawks": "seattle seahawks",
        "bucs": "tampa bay buccaneers",
        "buccaneers": "tampa bay buccaneers",
        "titans": "tennessee titans",
        "commanders": "washington commanders",
        "washington football team": "washington commanders",
        
        # NBA
        "hawks": "atlanta hawks",
        "celtics": "boston celtics",
        "nets": "brooklyn nets",
        "hornets": "charlotte hornets",
        "bulls": "chicago bulls",
        "cavaliers": "cleveland cavaliers",
        "cavs": "cleveland cavaliers",
        "mavs": "dallas mavericks",
        "mavericks": "dallas mavericks",
        "nuggets": "denver nuggets",
        "pistons": "detroit pistons",
        "warriors": "golden state warriors",
        "rockets": "houston rockets",
        "pacers": "indiana pacers",
        "clippers": "los angeles clippers",
        "lakers": "los angeles lakers",
        "grizzlies": "memphis grizzlies",
        "heat": "miami heat",
        "bucks": "milwaukee bucks",
        "timberwolves": "minnesota timberwolves",
        "wolves": "minnesota timberwolves",
        "pelicans": "new orleans pelicans",
        "knicks": "new york knicks",
        "thunder": "oklahoma city thunder",
        "magic": "orlando magic",
        "sixers": "philadelphia 76ers",
        "76ers": "philadelphia 76ers",
        "suns": "phoenix suns",
        "blazers": "portland trail blazers",
        "trail blazers": "portland trail blazers",
        "kings": "sacramento kings",
        "spurs": "san antonio spurs",
        "raptors": "toronto raptors",
        "jazz": "utah jazz",
        "wizards": "washington wizards",
        
        # NHL
        "ducks": "anaheim ducks",
        "coyotes": "arizona coyotes",
        "bruins": "boston bruins",
        "sabres": "buffalo sabres",
        "flames": "calgary flames",
        "hurricanes": "carolina hurricanes",
        "blackhawks": "chicago blackhawks",
        "avalanche": "colorado avalanche",
        "blue jackets": "columbus blue jackets",
        "stars": "dallas stars",
        "red wings": "detroit red wings",
        "oilers": "edmonton oilers",
        "panthers": "florida panthers",
        "kings": "los angeles kings",
        "wild": "minnesota wild",
        "canadiens": "montreal canadiens",
        "habs": "montreal canadiens",
        "predators": "nashville predators",
        "preds": "nashville predators",
        "devils": "new jersey devils",
        "islanders": "new york islanders",
        "rangers": "new york rangers",
        "senators": "ottawa senators",
        "sens": "ottawa senators",
        "flyers": "philadelphia flyers",
        "penguins": "pittsburgh penguins",
        "pens": "pittsburgh penguins",
        "sharks": "san jose sharks",
        "kraken": "seattle kraken",
        "blues": "st. louis blues",
        "lightning": "tampa bay lightning",
        "bolts": "tampa bay lightning",
        "maple leafs": "toronto maple leafs",
        "leafs": "toronto maple leafs",
        "canucks": "vancouver canucks",
        "golden knights": "vegas golden knights",
        "knights": "vegas golden knights",
        "capitals": "washington capitals",
        "caps": "washington capitals",
        "jets": "winnipeg jets",
        
        # EPL
        "gunners": "arsenal",
        "villa": "aston villa",
        "cherries": "bournemouth",
        "bees": "brentford",
        "seagulls": "brighton",
        "clarets": "burnley",
        "blues": "chelsea",
        "eagles": "crystal palace",
        "toffees": "everton",
        "cottagers": "fulham",
        "tractor boys": "ipswich",
        "foxes": "leicester",
        "reds": "liverpool",
        "hatters": "luton",
        "citizens": "manchester city",
        "city": "manchester city",
        "united": "manchester united",
        "man utd": "manchester united",
        "man united": "manchester united",
        "man city": "manchester city",
        "magpies": "newcastle united",
        "forest": "nottingham forest",
        "blades": "sheffield united",
        "saints": "southampton",
        "spurs": "tottenham hotspur",
        "hammers": "west ham united",
        "wanderers": "wolverhampton wanderers"
    }
    
    # Check for special cases (abbreviations and common names)
    if team_name_lower in special_cases:
        team_name_lower = special_cases[team_name_lower]
    
    # Exact match
    if team_name_lower in logo_database:
        return logo_database[team_name_lower]
    
    # Partial match
    for team, logo in logo_database.items():
        if team_name_lower in team or team in team_name_lower:
            return logo
    
    # If no match, try constructing URLs based on team/league patterns
    if league:
        # Keep your current league-specific URL construction code
        pass  # Placeholder for league-specific URL construction logic
    
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
        
        # Important: Get the direct URL to the team's page on TheSportsDB
        team_url = f"https://www.thesportsdb.com/team/{team_id}-{team_name.lower().replace(' ', '-')}"
        
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
        
        # If we still don't have a logo, try direct TheSportsDB URL format
        if not logo_url:
            # This is a common format TheSportsDB uses
            direct_url = f"https://www.thesportsdb.com/images/media/team/badge/{team_id}.png"
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.head(direct_url, timeout=1, headers=headers)
                if response.status_code == 200:
                    logo_url = direct_url
            except:
                pass
        
        # If still no logo, try dynamic logo generation
        if not logo_url:
            logo_url = generate_team_logo_url(team_name, league, team_id)
        
        return {
            "team": team_name,
            "league": league,
            "stadium": team.get("strStadium", "Unknown Stadium"),
            "team_id": team_id,
            "logo": logo_url,
            "banner": team.get("strTeamBanner", ""),
            "description": team.get("strDescriptionEN", ""),
            "website": team.get("strWebsite", ""),
            "thesportsdb_url": team_url  # Add this for debugging
        }
    else:
        # Try a more advanced search for teams with non-exact match
        return advanced_team_search(team_name)

def advanced_team_search(team_name):
    """Try to find teams that might not match exact search"""
    # Try search with just the first word (for teams like "Philadelphia Eagles")
    first_word = team_name.split()[0] if team_name and ' ' in team_name else team_name
    url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/searchteams.php?t={first_word}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("teams") and len(data["teams"]) > 0:
            # Look for a team that contains our search string
            full_name_lower = team_name.lower()
            for team in data["teams"]:
                team_name_api = team.get("strTeam", "").lower()
                if full_name_lower in team_name_api or team_name_api in full_name_lower:
                    # Found a match! Process it like in get_team_details
                    team_id = team.get("idTeam", "")
                    team_name = team.get("strTeam", "")
                    league = team.get("strLeague", "")
                    team_url = f"https://www.thesportsdb.com/team/{team_id}-{team_name.lower().replace(' ', '-')}"
                    
                    logo_url = team.get("strTeamBadge", "")
                    if not logo_url:
                        logo_url = team.get("strTeamLogo", "")
                    if not logo_url:
                        logo_url = team.get("strTeamJersey", "")
                    if not logo_url:
                        logo_url = get_team_logo(team_name, league)
                    if not logo_url:
                        logo_url = generate_team_logo_url(team_name, league, team_id)
                    
                    return {
                        "team": team_name,
                        "league": league,
                        "stadium": team.get("strStadium", "Unknown Stadium"),
                        "team_id": team_id,
                        "logo": logo_url,
                        "banner": team.get("strTeamBanner", ""),
                        "description": team.get("strDescriptionEN", ""),
                        "website": team.get("strWebsite", ""),
                        "thesportsdb_url": team_url,
                        "search_method": "advanced_match"  # Mark this as from advanced search
                    }
    except:
        pass
    
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
    
    # Direct TheSportsDB URL
    logo_urls.append(f"https://www.thesportsdb.com/images/media/team/badge/{team_id}.png")
    
    # TheSportsDB formats
    logo_urls.extend([
        f"https://www.thesportsdb.com/images/media/team/logo/{team_name_underscore}.png",
        f"https://www.thesportsdb.com/images/media/team/badge/{team_name_simple}.png",
        f"https://www.thesportsdb.com/images/media/team/logo/{team_id}.png"
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
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{team_name_clean}.png",
            f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"
        ])
    
    elif "nfl" in league_lower or "american football" in league_lower:
        # Extract team city and nickname for NFL
        parts = team_name.split()
        if len(parts) >= 2:
            team_city = parts[0].lower()
            nickname = parts[-1].lower()
            
            # NFL team abbreviations
            nfl_abbrevs = {
                "cardinals": "ARI", "falcons": "ATL", "ravens": "BAL", "bills": "BUF",
                "panthers": "CAR", "bears": "CHI", "bengals": "CIN", "browns": "CLE",
                "cowboys": "DAL", "broncos": "DEN", "lions": "DET", "packers": "GB",
                "texans": "HOU", "colts": "IND", "jaguars": "JAX", "chiefs": "KC",
                "chargers": "LAC", "rams": "LA", "dolphins": "MIA", "vikings": "MIN",
                "patriots": "NE", "saints": "NO", "giants": "NYG", "jets": "NYJ",
                "raiders": "LV", "eagles": "PHI", "steelers": "PIT", "seahawks": "SEA",
                "49ers": "SF", "buccaneers": "TB", "titans": "TEN", "commanders": "WAS"
            }
            
            team_abbr = nfl_abbrevs.get(nickname, team_name_clean[:3].upper())
            
            logo_urls.extend([
                f"https://static.www.nfl.com/t_q-best/league/api/clubs/logos/{team_abbr}",
                f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{team_abbr.lower()}.png",
                f"https://static.www.nfl.com/image/private/f_auto/league/api/clubs/logos/{team_abbr}"
            ])
    
    elif "mlb" in league_lower or "baseball" in league_lower:
        # Extract team nickname for MLB
        parts = team_name.split()
        nickname = parts[-1].lower() if len(parts) >= 2 else team_name.lower()
        
        # MLB team IDs
        mlb_ids = {
            "angels": "108", "astros": "117", "athletics": "133", "blue jays": "141",
            "braves": "144", "brewers": "158", "cardinals": "138", "cubs": "112",
            "diamondbacks": "109", "dodgers": "119", "giants": "137", "guardians": "114",
            "indians": "114", "mariners": "136", "marlins": "146", "mets": "121",
            "nationals": "120", "orioles": "110", "padres": "135", "phillies": "143",
            "pirates": "134", "rangers": "140", "rays": "139", "red sox": "111",
            "reds": "113", "rockies": "115", "royals": "118", "tigers": "116",
            "twins": "142", "white sox": "145", "yankees": "147"
        }
        
        team_id_mlb = mlb_ids.get(nickname.lower(), "")
        if team_id_mlb:
            logo_urls.extend([
                f"https://www.mlbstatic.com/team-logos/team-cap-on-light/{team_id_mlb}.svg",
                f"https://www.mlbstatic.com/team-logos/{team_id_mlb}.svg"
            ])
        
        logo_urls.extend([
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/{team_name_clean}.png",
            f"https://img.mlbstatic.com/mlb-images/image/upload/t_16x9/t_w1536/mlb/pj3g19guppubo5hfsklb.jpg"
        ])
    
    elif "nhl" in league_lower or "hockey" in league_lower:
        # Extract team nickname for NHL
        parts = team_name.split()
        nickname = parts[-1].lower() if len(parts) >= 2 else team_name.lower()
        
        # NHL team abbreviations
        nhl_abbrevs = {
            "ducks": "ANA", "coyotes": "ARI", "bruins": "BOS", "sabres": "BUF",
            "flames": "CGY", "hurricanes": "CAR", "blackhawks": "CHI", "avalanche": "COL",
            "blue jackets": "CBJ", "stars": "DAL", "red wings": "DET", "oilers": "EDM",
            "panthers": "FLA", "kings": "LAK", "wild": "MIN", "canadiens": "MTL",
            "predators": "NSH", "devils": "NJD", "islanders": "NYI", "rangers": "NYR",
            "senators": "OTT", "flyers": "PHI", "penguins": "PIT", "sharks": "SJS",
            "kraken": "SEA", "blues": "STL", "lightning": "TBL", "maple leafs": "TOR",
            "canucks": "VAN", "golden knights": "VGK", "capitals": "WSH", "jets": "WPG"
        }
        
        # Try to match by nickname or team name
        team_abbr = ""
        for key, abbr in nhl_abbrevs.items():
            if key in team_name.lower():
                team_abbr = abbr
                break
        
        if not team_abbr and nickname in nhl_abbrevs:
            team_abbr = nhl_abbrevs[nickname]
        
        if team_abbr:
            logo_urls.extend([
                f"https://assets.nhle.com/logos/nhl/svg/{team_abbr}_light.svg",
                f"https://www.nhl.com/{team_name_clean}/prod/images/logos/logo.svg"
            ])
        
        logo_urls.extend([
            f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nhl/500/{team_name_clean}.png"
        ])
    
    # Generic ESPN pattern as fallback (works for many teams)
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

def generate_response(user_query, info_type="all"):
    """Generate a response to sports-related queries"""
    # Check if this is a team-specific query
    team_info = get_team_info(user_query)
    
    if team_info:
        # Continue with existing team-specific logic
        return generate_team_response(user_query, info_type)
    else:
        # This is a general sports question
        return generate_general_sports_response(user_query)

def generate_team_response(team_name, info_type="all"):
    """Get team info and pass it to Ollama for a conversational reply"""
    team_info = get_team_info(team_name)
    
    if not team_info:
        return "Sorry, I couldn't find that team."
    
    # Rest of your existing team response code
    # ...

def generate_general_sports_response(query):
    """Generate response for general sports questions"""
    # Format a prompt for the LLM with the user's query
    prompt = f"""
You are SportsChat, an AI sports announcer specializing in the NFL, NHL, MLB, NBA, and English Premier League.

The user has asked: "{query}"

Answer the query comprehensively with your sports knowledge. Include:
- Relevant statistics and historical context
- Player achievements and records if applicable
- Team histories if relevant
- Recent developments in that sports topic
- Citations to well-known sports events or moments

Use a conversational, enthusiastic sports announcer style.

Important: If the question is about a specific athlete, team, game, or sports record, provide detailed information about that specific topic. If you don't have enough information about a specific detail, acknowledge this limitation but still provide the general information you do know.
"""
    
    # Pass to the LLM
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
