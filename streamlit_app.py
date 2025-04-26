import streamlit as st
import main as sports_app

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

# Display chat history
chat_container = st.container()
with chat_container:
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"**You:** {entry['content']}")
            st.markdown("---")
        else:
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
    # Add user query to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": f"Tell me about {team_name} ({info_type.lower()})"
    })
    
    with st.spinner(f"Getting info about {team_name}..."):
        response = sports_app.generate_response(team_name, info_map[info_type])
        
        # Add response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Show raw data in expandable section
        team_info = sports_app.get_team_info(team_name)
        if team_info:
            with st.expander("Raw Data"):
                st.write("Team Info:")
                st.json(team_info)
                
                if info_type in ["All Information", "Latest Results"]:
                    results = sports_app.get_latest_results(team_info["team_id"])
                    st.write("Latest Results:")
                    st.json(results)
                
                if info_type in ["All Information", "Upcoming Fixtures"]:
                    fixtures = sports_app.get_upcoming_matches(team_info["team_id"])
                    st.write("Upcoming Fixtures:")
                    st.json(fixtures)
                
                if info_type in ["All Information", "League Standings"]:
                    league_id = sports_app.get_league_id(team_info["team_id"])
                    if league_id:
                        standings = sports_app.get_league_standings(league_id)
                        st.write(f"League Standings (ID: {league_id}):")
                        st.json(standings)
    
    # Rerun to update the chat display
    st.rerun()