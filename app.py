import streamlit as st

st.set_page_config(page_title="Dota 2 AI Assistant")

st.title("Dota 2 AI Assistant (MVP)")
st.write("Console logic wrapped into a simple web interface.")

enemy_heroes = st.multiselect(
    "Select enemy heroes:",
    [
        "Phantom Assassin",
        "Lion",
        "Zeus",
        "Axe",
        "Juggernaut"
    ]
)

if st.button("Analyze"):
    st.subheader("AI Recommendation")

    if "Phantom Assassin" in enemy_heroes:
        st.write("• Buy **Monkey King Bar** (evasion counter)")
    if "Lion" in enemy_heroes:
        st.write("• Buy **Black King Bar** (strong disables)")
    if "Zeus" in enemy_heroes:
        st.write("• Consider **Pipe of Insight** (magic damage)")

    if not enemy_heroes:
        st.write("Please select at least one enemy hero.")
