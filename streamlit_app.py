import streamlit as st
import main as sports_app
import requests

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="SportsChat", page_icon="🏆", layout="wide")

# Update the title and description
st.title("SportsChat 🏆")
st.write("Your AI sports assistant for NFL, NBA, MLB, NHL and Premier League. Ask about teams, players, records, or any sports trivia!")

# Add a section with example questions
with st.expander("Example questions you can ask"):
    st.markdown("""
    * Who won the most Super Bowl rings?
    * Which team has the most NBA championships?
    * Tell me about Manchester United's history
    * Who holds the MLB home run record?
    * When was the last time the Chicago Cubs won the World Series?
    * Which quarterback has thrown the most touchdown passes?
    * Who are the greatest NHL players of all time?
    * What team has the most English Premier League titles?
    * Tell me about Michael Jordan's career achievements
    * What were the biggest upsets in Super Bowl history?
    """)

# Add an "About" expander
with st.expander("About SportsChat"):
    st.markdown("""
    **SportsChat** is a sports AI assistant that can answer questions about:
    
    * **Teams**: Get information, latest results, upcoming fixtures and league standings
    * **Players**: Learn about current and legendary players across major leagues
    * **Records**: Find out about championships, individual achievements and historical moments
    * **Live Data**: Get recent game results and upcoming fixtures
    * **History**: Explore the rich history of NFL, NBA, MLB, NHL and English Premier League
    
    SportsChat uses real-time data for team information and LLM capabilities to answer general sports questions from its knowledge base.
    """)

# Sidebar for options
with st.sidebar:
    st.header("Information Type")
    info_type = st.radio(
        "Choose what information to display:",
        ["All Information", "Team Information", "Latest Results", "Upcoming Fixtures", "League Standings"]
    )
    
    st.header("Select a Team")
    
    # Create a dropdown for leagues
    league_options = [
        "English Premier League (Soccer)",
        "NBA (Basketball)",
        "NFL (American Football)",
        "MLB (Baseball)",
        "NHL (Hockey)"
    ]
    
    selected_league = st.selectbox("Select a League", league_options)
    
    # Define teams by league with their full names and nicknames
    league_teams = {
        "English Premier League (Soccer)": {
            "Arsenal": "Arsenal",
            "Aston Villa": "Aston Villa",
            "Bournemouth": "Bournemouth",
            "Brentford": "Brentford",
            "Brighton": "Brighton",
            "Burnley": "Burnley",
            "Chelsea": "Chelsea",
            "Crystal Palace": "Crystal Palace",
            "Everton": "Everton",
            "Fulham": "Fulham",
            "Ipswich": "Ipswich",
            "Liverpool": "Liverpool",
            "Man City": "Manchester City",
            "Man United": "Manchester United",
            "Newcastle": "Newcastle United",
            "Nottingham": "Nottingham Forest",
            "Tottenham": "Tottenham Hotspur",
            "West Ham": "West Ham United",
            "Wolves": "Wolverhampton"
        },
        "NBA (Basketball)": {
            "Lakers": "Los Angeles Lakers",
            "Celtics": "Boston Celtics",
            "Warriors": "Golden State Warriors",
            "Bulls": "Chicago Bulls",
            "Heat": "Miami Heat",
            "Knicks": "New York Knicks",
            "76ers": "Philadelphia 76ers",
            "Suns": "Phoenix Suns",
            "Nets": "Brooklyn Nets",
            "Clippers": "LA Clippers",
            "Mavs": "Dallas Mavericks",
            "Bucks": "Milwaukee Bucks",
            "Raptors": "Toronto Raptors",
            "Nuggets": "Denver Nuggets",
            "Hawks": "Atlanta Hawks",
            "Spurs": "San Antonio Spurs"
        },
        "NFL (American Football)": {
            "Chiefs": "Kansas City Chiefs",
            "49ers": "San Francisco 49ers",
            "Cowboys": "Dallas Cowboys",
            "Eagles": "Philadelphia Eagles",
            "Patriots": "New England Patriots",
            "Packers": "Green Bay Packers",
            "Bills": "Buffalo Bills",
            "Ravens": "Baltimore Ravens",
            "Buccaneers": "Tampa Bay Buccaneers",
            "Rams": "Los Angeles Rams",
            "Steelers": "Pittsburgh Steelers",
            "Seahawks": "Seattle Seahawks",
            "Bears": "Chicago Bears",
            "Broncos": "Denver Broncos",
            "Vikings": "Minnesota Vikings",
            "Saints": "New Orleans Saints"
        },
        "MLB (Baseball)": {
            "Yankees": "New York Yankees",
            "Red Sox": "Boston Red Sox",
            "Dodgers": "Los Angeles Dodgers",
            "Cubs": "Chicago Cubs",
            "Giants": "San Francisco Giants",
            "Cardinals": "St. Louis Cardinals",
            "Braves": "Atlanta Braves",
            "Astros": "Houston Astros",
            "Mets": "New York Mets",
            "Blue Jays": "Toronto Blue Jays",
            "Phillies": "Philadelphia Phillies",
            "Padres": "San Diego Padres",
            "D-backs": "Arizona Diamondbacks",
            "Mariners": "Seattle Mariners",
            "Twins": "Minnesota Twins",
            "Tigers": "Detroit Tigers"
        },
        "NHL (Hockey)": {
            "Maple Leafs": "Toronto Maple Leafs",
            "Canadiens": "Montreal Canadiens",
            "Rangers": "New York Rangers",
            "Bruins": "Boston Bruins",
            "Blackhawks": "Chicago Blackhawks",
            "Red Wings": "Detroit Red Wings",
            "Penguins": "Pittsburgh Penguins",
            "Lightning": "Tampa Bay Lightning",
            "Oilers": "Edmonton Oilers",
            "Flames": "Calgary Flames",
            "Canucks": "Vancouver Canucks",
            "Golden Knights": "Vegas Golden Knights",
            "Avalanche": "Colorado Avalanche",
            "Capitals": "Washington Capitals",
            "Flyers": "Philadelphia Flyers",
            "Kraken": "Seattle Kraken"
        }
    }
    
    # Get teams for the selected league
    teams_for_league = league_teams.get(selected_league, {})
    team_nicknames = list(teams_for_league.keys())
    
    # Display team dropdown with logos
    selected_nickname = st.selectbox(
        f"Select a {selected_league.split(' ')[0]} Team:",
        team_nicknames,
        format_func=lambda x: x
    )
    
    # Get the full team name from the nickname
    if selected_nickname:
        full_team_name = teams_for_league[selected_nickname]
        
        # Get logo URL
        team_logo = sports_app.get_team_logo(full_team_name)
        
        # Display logo and team name
        st.write("Selected Team:")
        
        # Create a container with columns for the logo and team name
        cols = st.columns([1, 3])
        with cols[0]:
            if team_logo:
                st.image(team_logo, width=70)
            else:
                sport_icon = get_sport_icon(selected_league)
                st.markdown(f"<h1 style='font-size: 2.5rem; margin: 0;'>{sport_icon}</h1>", unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"<h3 style='margin-top:10px;'>{full_team_name}</h3>", unsafe_allow_html=True)
        
        # Add a Get Info button
        if st.button("Get Info About This Team"):
            st.session_state.team_input = full_team_name
    
    # Keep the Clear Chat History button at the bottom
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.team_input = ""

info_map = {
    "All Information": "all",
    "Team Information": "basic",
    "Latest Results": "results", 
    "Upcoming Fixtures": "fixtures",
    "League Standings": "standings"
}

# Helper function to determine sport icon
def get_sport_icon(league_name):
    """Return an appropriate emoji based on the league/sport"""
    league_name = league_name.lower() if league_name else ""
    
    if any(x in league_name for x in ["soccer", "football", "premier", "la liga", "bundesliga", "serie a"]):
        return "⚽"
    elif any(x in league_name for x in ["nba", "basketball", "ncaa"]):
        return "🏀"
    elif any(x in league_name for x in ["nhl", "hockey", "ice"]):
        return "🏒"
    elif any(x in league_name for x in ["mlb", "baseball"]):
        return "⚾"
    elif any(x in league_name for x in ["nfl", "american football"]):
        return "🏈"
    else:
        return "🏆"

# Display chat history with logos or sport-specific icons
chat_container = st.container()
with chat_container:
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"**You:** {entry['content']}")
            st.markdown("---")
        else:
            col1, col2 = st.columns([2, 8])  # Changed from [1, 10] to [2, 8] to give more space for the logo
            with col1:
                if "logo" in entry and entry["logo"]:
                    try:
                        # Add headers to avoid some blocking issues
                        headers = {"User-Agent": "Mozilla/5.0"}
                        # Increase logo size from 50 to 100 pixels
                        st.image(entry["logo"], width=200)
                    except Exception as e:
                        # If logo doesn't load, use sport-specific icon based on league
                        league = entry.get("league", "") if "league" in entry else ""
                        icon = get_sport_icon(league)
                        # Make the emoji larger too
                        st.markdown(f"<h1 style='font-size: 8rem; margin: 0;'>{icon}</h1>", unsafe_allow_html=True)
                        # Optional: add debug comment for understanding why it failed
                        st.markdown(f"<!-- Logo failed: {str(e)} -->", unsafe_allow_html=True)
                else:
                    # No logo, display a generic sports icon
                    st.markdown("<h1 style='font-size: 4rem; margin: 0;'>🏆</h1>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**SportsChat:** {entry['content']}")
            st.markdown("---")

# Handle user input
if "team_input" not in st.session_state:
    st.session_state.team_input = ""

# Use custom CSS to improve alignment
st.markdown("""
<style>
    .stButton > button {
        height: 3.125rem;
        margin-top: 0px;
    }
    .input-container {
        display: flex;
        align-items: center;
    }
    .input-container > div:first-child {
        flex-grow: 1;
        margin-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Create a container for the input field and button with flexbox styling
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Column for input field
col1, col2 = st.columns([5, 1])
with col1:
    # Update the placeholder text for input
    team_name = st.text_input("Ask about a team or any sports question:", 
                             value=st.session_state.team_input, 
                             placeholder="e.g., Arsenal, Who won the most Super Bowl rings?",
                             key="team_input_field")
with col2:
    # Add a small spacer to align the button with the input field
    st.write("")
    # Update the button label
    submit_button = st.button("Ask SportsChat")

st.markdown('</div>', unsafe_allow_html=True)

if submit_button and team_name:
    # First, check if this appears to be a question (contains a question word or ends with '?')
    question_words = ["who", "what", "when", "where", "why", "how", "which", "can", "did", "does", "is", "are", "will"]
    is_question = team_name.lower().split()[0] in question_words or team_name.endswith('?') or len(team_name.split()) > 5
    
    # Add user query to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": team_name
    })
    
    # Initialize team_info to None before the if/else branches
    team_info = None
    
    with st.spinner(f"Getting information..."):
        if is_question:
            # This is likely a general sports question
            response = sports_app.generate_general_sports_response(team_name)
            
            # Add generic sport logo based on the question content
            sport_type = "unknown"
            if any(word in team_name.lower() for word in ["nfl", "football", "super bowl", "touchdown"]):
                sport_type = "NFL (American Football)"
            elif any(word in team_name.lower() for word in ["nba", "basketball", "dunk", "court"]):
                sport_type = "NBA (Basketball)"
            elif any(word in team_name.lower() for word in ["mlb", "baseball", "homerun", "pitcher"]):
                sport_type = "MLB (Baseball)"
            elif any(word in team_name.lower() for word in ["nhl", "hockey", "puck", "stanley cup"]):
                sport_type = "NHL (Hockey)"
            elif any(word in team_name.lower() for word in ["epl", "premier league", "soccer", "football", "goal"]):
                sport_type = "English Premier League (Soccer)"
            
            logo_url = ""  # Default empty logo
            league_name = sport_type
            
            # Add response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
                "logo": logo_url,
                "league": league_name
            })
        else:
            # Original team-based flow
            team_info = sports_app.get_team_info(team_name)
            logo_url = team_info.get("logo", "") if team_info else ""
            
            if team_info:
                # Generate response and add to chat history as before
                response = sports_app.generate_response(team_name, info_map[info_type])
                
                # Add response to chat history with logo and league info
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "logo": logo_url,
                    "league": team_info.get("league", "")
                })
            else:
                # Handle case where team is not found but it's not detected as a question
                # Try generating a general response instead
                response = sports_app.generate_general_sports_response(team_name)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "logo": "",
                    "league": "unknown"
                })
        
        # After adding the response to the chat history
        # Only check for fixtures if team_info exists
        if team_info:
            # Check if there's at least one relevant fixture
            has_relevant_fixtures = False
            if info_type in ["All Information", "Upcoming Fixtures"]:
                fixtures = sports_app.get_upcoming_matches(team_info["team_id"])
                for fixture in fixtures:
                    if (team_info["team"].lower() in fixture["home_team"].lower() or 
                        team_info["team"].lower() in fixture["away_team"].lower()):
                        has_relevant_fixtures = True
                        break
                
                if not has_relevant_fixtures and fixtures:
                    st.warning(f"⚠️ Some fixtures shown may not be relevant to {team_info['team']}. TheSportsDB API sometimes returns generic fixtures when team-specific data is unavailable.")
        
            # Show raw data in expandable section, but only if team_info exists
            with st.expander("Raw Data"):
                st.write("Team Info:")
                st.json(team_info)
                
                if info_type in ["All Information", "Latest Results"]:
                    results = sports_app.get_latest_results(team_info["team_id"])
                    st.write("Latest Results:")
                    st.json(results)
                    
                    # Debug to check for team name consistency
                    team_name_val = team_info["team"]
                    st.write(f"Checking if results are relevant to {team_name_val}:")
                    for result in results:
                        is_relevant = (team_name_val.lower() in result["home_team"].lower() or 
                                      team_name_val.lower() in result["away_team"].lower())
                        st.write(f"- {result['home_team']} vs {result['away_team']}: {'✅' if is_relevant else '❌'}")
                
                if info_type in ["All Information", "Upcoming Fixtures"]:
                    fixtures = sports_app.get_upcoming_matches(team_info["team_id"])
                    st.write("Upcoming Fixtures:")
                    st.json(fixtures)
                    
                    # Debug to check for team name consistency
                    st.write(f"Checking if fixtures are relevant to {team_name_val}:")
                    for fixture in fixtures:
                        is_relevant = (team_name_val.lower() in fixture["home_team"].lower() or 
                                      team_name_val.lower() in fixture["away_team"].lower())
                        st.write(f"- {fixture['home_team']} vs {fixture['away_team']}: {'✅' if is_relevant else '❌'}")
                
                if info_type in ["All Information", "League Standings"]:
                    league_id = sports_app.get_league_id(team_info["team_id"])
                    if league_id:
                        standings = sports_app.get_league_standings(league_id)
                        st.write(f"League Standings (ID: {league_id}):")
                        st.json(standings)
    
    # Rerun to update the chat display
    st.rerun()