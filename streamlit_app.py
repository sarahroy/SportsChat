import streamlit as st
import main as sports_app

st.set_page_config(page_title="SportsChat", page_icon="🏆")

st.title("SportsChat 🏆")
st.write("Get real-time sports updates in a conversational format")

# Sidebar for options
st.sidebar.header("Information Type")
info_type = st.sidebar.radio(
    "Choose what information to display:",
    ["All Information", "Team Information", "Latest Results", "Upcoming Fixtures", "League Standings"]
)

info_map = {
    "All Information": "all",
    "Team Information": "basic",
    "Latest Results": "results", 
    "Upcoming Fixtures": "fixtures",
    "League Standings": "standings"
}

# Handle user input
team_name = st.text_input("Enter a team name:", placeholder="e.g., Arsenal, Los Angeles Lakers")

if st.button("Get Info") and team_name:
    with st.spinner(f"Getting info about {team_name}..."):
        response = sports_app.generate_response(team_name, info_map[info_type])
        
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
        
        # Display the conversational response
        st.markdown("### Response")
        st.write(response)
        
# Show example teams
st.markdown("---")
st.markdown("### Example teams to try:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**Soccer/Football:**")
    st.write("Arsenal")
    st.write("Manchester United")
    st.write("Liverpool")
with col2:
    st.markdown("**Basketball:**")
    st.write("Los Angeles Lakers")
    st.write("Boston Celtics")
    st.write("Chicago Bulls")
with col3:
    st.markdown("**Hockey:**")
    st.write("Toronto Maple Leafs")
    st.write("New York Rangers")
    st.write("Boston Bruins")
with col4:
    st.markdown("**American Football:**")
    st.write("Kansas City Chiefs")
    st.write("Dallas Cowboys")
    st.write("Green Bay Packers")