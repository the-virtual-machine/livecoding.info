import streamlit as st
import pandas as pd
from datetime import datetime

st.header("Livecoding.info")


# Load CSV file
df = pd.read_csv('info.csv')

# Initialize the 'Start Date' column if it doesn't exist
if 'Start Date' not in df.columns:
    df['Start Date'] = None

# List of tools for each category
audio_tools = ["Sonic Pi", "TidalCycles", "FoxDot", "Orca"]
visual_tools = ["Hydra", "Live Code Lab", "Visor", "P5LIVE"]
other_tools = ["Arcadia", "bl4st", "DanceDirt", "Kairos", "La Habra", "Polonium", "The Force", "The Dark Side", "Thixels"]

# Function to display artists by category and tool
def display_artists(category, tool):
    filtered_df = df[df['Category'].apply(lambda x: category in x) & df['Tool'].apply(lambda x: tool in x)]
    if 'Start Date' in filtered_df.columns:
        filtered_df['Years Livecoding'] = filtered_df['Start Date'].apply(lambda x: (datetime.now() - datetime.strptime(x, '%Y-%m-%d')).days // 365 if pd.notnull(x) else 0)
    st.dataframe(filtered_df[['Name', 'Years Livecoding', 'Description', 'Repo Link']])

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
st.sidebar.write("Version: 0.1 - 28th July 2024")
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
        st.session_state.selected_tools.extend(show_tools(audio_tools, "audio"))
    
    if visual_selected:
        st.subheader("Visual Tools")
        st.session_state.selected_tools.extend(show_tools(visual_tools, "visual"))
    
    if other_selected:
        st.subheader("Other Tools")
        st.session_state.selected_tools.extend(show_tools(other_tools, "other"))

    name = st.text_input("Name")
    start_date = st.date_input("Start Date (YYYY-MM-DD)")
    description = st.text_area("Description")
    repo_link = st.text_input("Repo Link")
    submitted = st.form_submit_button("Submit")
    if submitted:
        new_entry = pd.DataFrame({
            'Name': [name],
            'Category': [list(set(["Audio" if t in audio_tools else "Visual" if t in visual_tools else "Other" for t in st.session_state.selected_tools]))],
            'Tool': [st.session_state.selected_tools],
            'Description': [description],
            'Repo Link': [repo_link],
            'Start Date': [start_date.strftime('%Y-%m-%d')]
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
