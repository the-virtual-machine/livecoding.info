import streamlit as st
import pandas as pd

# Load CSV file
df = pd.read_csv('info.csv')

# List of tools for each category
audio_tools = ["Sonic Pi", "TidalCycles", "FoxDot", "Orca"]
visual_tools = ["Hydra", "Live Code Lab", "Visor", "P5LIVE"]
other_tools = ["Arcadia", "bl4st", "DanceDirt", "Kairos", "La Habra", "Polonium", "The Force", "The Dark Side", "Thixels"]

# Function to display artists by category and tool
def display_artists(category, tool):
    filtered_df = df[(df['Category'] == category) & (df['Tool'] == tool)]
    st.dataframe(filtered_df)

# Tabs for categories
tabs = st.tabs(["Audio Livecoders", "Visual Livecoders"])

# Audio Livecoders Tab
with tabs[0]:
    audio_tabs = st.tabs(audio_tools)
    for i, tool in enumerate(audio_tools):
        with audio_tabs[i]:
            display_artists("Audio", tool)

# Visual Livecoders Tab
with tabs[1]:
    visual_tabs = st.tabs(visual_tools)
    for i, tool in enumerate(visual_tools):
        with visual_tabs[i]:
            display_artists("Visual", tool)

# Initialize session state
if 'selected_tools' not in st.session_state:
    st.session_state.selected_tools = []

# Sidebar Submission Form
st.sidebar.header("Submit Your Info")

audio_selected = st.sidebar.checkbox("Audio")
visual_selected = st.sidebar.checkbox("Visual")
other_selected = st.sidebar.checkbox("Other")

def show_tools(tools, category_key):
    selected = []
    for tool in tools:
        if st.checkbox(tool, key=f"{category_key}_{tool}"):
            selected.append(tool)
    return selected

with st.sidebar.form("submit_form"):
    if audio_selected:
        st.subheader("Audio Tools")
        selected_audio_tools = show_tools(audio_tools, "audio")
        st.session_state.selected_tools.extend(selected_audio_tools)
    
    if visual_selected:
        st.subheader("Visual Tools")
        selected_visual_tools = show_tools(visual_tools, "visual")
        st.session_state.selected_tools.extend(selected_visual_tools)
    
    if other_selected:
        st.subheader("Other Tools")
        selected_other_tools = show_tools(other_tools, "other")
        st.session_state.selected_tools.extend(selected_other_tools)

    name = st.text_input("Name")
    description = st.text_area("Description")
    repo_link = st.text_input("Repo Link")
    submitted = st.form_submit_button("Submit")
    if submitted:
        for t in st.session_state.selected_tools:
            new_entry = pd.DataFrame({
                'Name': [name],
                'Category': ["Audio" if t in audio_tools else "Visual" if t in visual_tools else "Other"],
                'Tool': [t],
                'Description': [description],
                'Repo Link': [repo_link]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv('info.csv', index=False)
        st.sidebar.success("Submission successful!")
        st.session_state.selected_tools = []

# Download Button in Sidebar
st.sidebar.header("Download Data")
st.sidebar.download_button("Download CSV", df.to_csv(index=False), "info.csv")

# Display CSV in Main Page
st.header("Current Artists")
st.dataframe(df)
