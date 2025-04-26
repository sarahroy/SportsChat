import streamlit as st
import main as sports_app
import requests

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="SportsChat", page_icon="🏆", layout="wide")

st.title("SportsChat 🏆")
st.write("Get real-time sports updates in a conversational format")

# Sidebar for options
with st.sidebar:
    st.header("Information Type")
    info_type = st.radio(
        "Choose what information to display:",
        ["All Information", "Team Information", "Latest Results", "Upcoming Fixtures", "League Standings"]
    )
    
    st.header("Examples")
    st.subheader("Soccer/Football:")
    if st.button("Arsenal"):
        st.session_state.team_input = "Arsenal"
    if st.button("Manchester United"):
        st.session_state.team_input = "Manchester United"
    if st.button("Liverpool"):
        st.session_state.team_input = "Liverpool"
    
    st.subheader("Basketball:")
    if st.button("Los Angeles Lakers"):
        st.session_state.team_input = "Los Angeles Lakers"
    if st.button("Boston Celtics"):
        st.session_state.team_input = "Boston Celtics"
    
    st.subheader("Hockey:")
    if st.button("Toronto Maple Leafs"):
        st.session_state.team_input = "Toronto Maple Leafs"
    
    st.subheader("American Football:")
    if st.button("Kansas City Chiefs"):
        st.session_state.team_input = "Kansas City Chiefs"
    
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
            col1, col2 = st.columns([1, 10])
            with col1:
                if "logo" in entry and entry["logo"]:
                    try:
                        # Add headers to avoid some blocking issues
                        headers = {"User-Agent": "Mozilla/5.0"}
                        st.image(entry["logo"], width=50)
                    except Exception as e:
                        # If logo doesn't load, use sport-specific icon based on league
                        league = entry.get("league", "") if "league" in entry else ""
                        icon = get_sport_icon(league)
                        st.markdown(f"<h1 style='font-size: 2.5rem; margin: 0;'>{icon}</h1>", unsafe_allow_html=True)
                        # Optional: add debug comment for understanding why it failed
                        st.markdown(f"<!-- Logo failed: {str(e)} -->", unsafe_allow_html=True)
                else:
                    # No logo, display a generic sports icon
                    st.markdown("<h1 style='font-size: 2.5rem; margin: 0;'>🏆</h1>", unsafe_allow_html=True)
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
    team_name = st.text_input("Enter a team name:", 
                             value=st.session_state.team_input, 
                             placeholder="e.g., Arsenal, Los Angeles Lakers",
                             key="team_input_field")
with col2:
    # Add a small spacer to align the button with the input field
    st.write("")
    submit_button = st.button("Get Info")

st.markdown('</div>', unsafe_allow_html=True)

if submit_button and team_name:
    # Get team info first
    team_info = sports_app.get_team_info(team_name)
    logo_url = team_info.get("logo", "") if team_info else ""
    
    # Debug the logo URL with more comprehensive information
    with st.expander("Debug Information"):
        st.write(f"Team name: {team_name}")
        st.write(f"Logo URL: {logo_url}")
        st.write("Team info:")
        st.json(team_info)
        
        # Show TheSportsDB direct URL if available
        if team_info and "thesportsdb_url" in team_info:
            st.write(f"TheSportsDB page: {team_info['thesportsdb_url']}")
        
        # Test multiple potential logo sources
        st.write("### Testing different logo sources:")
        
        # First try the main logo
        if logo_url:
            st.write("#### Main logo:")
            try:
                # Add User-Agent header to avoid blocking
                headers = {"User-Agent": "Mozilla/5.0"}
                st.image(logo_url, width=100)
                st.write("✅ Main logo loaded successfully!")
                
                # Try HEAD request to check URL status
                try:
                    head_response = requests.head(logo_url, timeout=2, headers=headers)
                    st.write(f"Status code: {head_response.status_code}")
                    st.write(f"Content type: {head_response.headers.get('Content-Type', 'Unknown')}")
                except Exception as e:
                    st.write(f"HEAD request failed: {str(e)}")
            except Exception as e:
                st.write(f"❌ Error loading main logo: {str(e)}")
        else:
            st.write("❌ No main logo URL found")
            
        # Test multiple potential sources
        if team_info:
            team_name_clean = team_info["team"].lower().replace(" ", "-")
            team_id = team_info["team_id"]
            league = team_info.get("league", "")
            
            st.write("#### Alternative logo sources:")
            alt_sources = [
                ("TheSportsDB Badge", f"https://www.thesportsdb.com/images/media/team/badge/{team_id}.png"),
                ("TheSportsDB Logo", f"https://www.thesportsdb.com/images/media/team/logo/{team_name_clean}.png"),
                ("ESPN Logo", f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/{team_name_clean}.png"),
                ("Premier League (if applicable)", f"https://resources.premierleague.com/premierleague/badges/t{team_id}.svg"),
            ]
            
            for source_name, url in alt_sources:
                st.write(f"**{source_name}**: {url}")
                try:
                    st.image(url, width=80)
                    st.write(f"✅ {source_name} loaded successfully!")
                    
                    # If main logo failed but this one works, use it
                    if not logo_url:
                        st.write("Using this as the main logo")
                        logo_url = url
                except:
                    st.write(f"❌ {source_name} failed to load")
    
    # Add user query to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": f"Tell me about {team_name} ({info_type.lower()})"
    })
    
    with st.spinner(f"Getting info about {team_name}..."):
        response = sports_app.generate_response(team_name, info_map[info_type])
        
        # Add response to chat history with logo and league info
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "logo": logo_url,
            "league": team_info.get("league", "") if team_info else ""
        })
        
        # After adding the response to the chat history
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
        
        # Show raw data in expandable section
        if team_info:
            with st.expander("Raw Data"):
                st.write("Team Info:")
                st.json(team_info)
                
                if info_type in ["All Information", "Latest Results"]:
                    results = sports_app.get_latest_results(team_info["team_id"])
                    st.write("Latest Results:")
                    st.json(results)
                    
                    # Debug to check for team name consistency
                    team_name = team_info["team"]
                    st.write(f"Checking if results are relevant to {team_name}:")
                    for result in results:
                        is_relevant = (team_name.lower() in result["home_team"].lower() or 
                                      team_name.lower() in result["away_team"].lower())
                        st.write(f"- {result['home_team']} vs {result['away_team']}: {'✅' if is_relevant else '❌'}")
                
                if info_type in ["All Information", "Upcoming Fixtures"]:
                    fixtures = sports_app.get_upcoming_matches(team_info["team_id"])
                    st.write("Upcoming Fixtures:")
                    st.json(fixtures)
                    
                    # Debug to check for team name consistency
                    st.write(f"Checking if fixtures are relevant to {team_name}:")
                    for fixture in fixtures:
                        is_relevant = (team_name.lower() in fixture["home_team"].lower() or 
                                      team_name.lower() in fixture["away_team"].lower())
                        st.write(f"- {fixture['home_team']} vs {fixture['away_team']}: {'✅' if is_relevant else '❌'}")
                
                if info_type in ["All Information", "League Standings"]:
                    league_id = sports_app.get_league_id(team_info["team_id"])
                    if league_id:
                        standings = sports_app.get_league_standings(league_id)
                        st.write(f"League Standings (ID: {league_id}):")
                        st.json(standings)
    
    # Rerun to update the chat display
    st.rerun()