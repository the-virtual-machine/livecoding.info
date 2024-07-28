import streamlit as st
import pandas as pd
import plotly.express as px
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

# Function to calculate years live coding
def calculate_years(start_date):
    if pd.isnull(start_date):
        return 0
    delta = datetime.now() - datetime.strptime(start_date, '%Y-%m-%d')
    return round(delta.days / 365.25, 1)

# Function to display artists by category and tool
def display_artists(category, tool):
    filtered_df = df[df['Category'].apply(lambda x: category in x) & df['Tool'].apply(lambda x: tool in x)].copy()
    if 'Start Date' in filtered_df.columns:
        filtered_df['Years Livecoding'] = filtered_df['Start Date'].apply(calculate_years)
    filtered_df['Category'] = filtered_df['Category'].apply(lambda x: ', '.join(x))
    filtered_df['Tool'] = filtered_df['Tool'].apply(lambda x: ', '.join(x))
    st.dataframe(filtered_df[['Name', 'Years Livecoding', 'Description', 'Repo Link']])

# Tabs for categories
tabs = st.tabs(["Audio Livecoders", "Visual Livecoders", "Other"])

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

# Other Livecoders Tab
with tabs[2]:
    other_tabs = st.tabs(other_tools)
    for i, tool in enumerate(other_tools):
        with other_tabs[i]:
            display_artists("Other", tool)

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
    start_date = st.date_input("Start Date")
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
df['Category'] = df['Category'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
df['Tool'] = df['Tool'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
st.dataframe(df)

# Data Analysis Section
st.header("Data Analysis")

# Calculate percentages for Audio, Visual, and Both categories
audio_count = df['Category'].apply(lambda x: 'Audio' in x).sum()
visual_count = df['Category'].apply(lambda x: 'Visual' in x).sum()
other_count = df['Category'].apply(lambda x: 'Other' in x).sum()
total = len(df)

st.write(f"Percentage of Audio Livecoders: {audio_count / total * 100:.2f}%")
st.write(f"Percentage of Visual Livecoders: {visual_count / total * 100:.2f}%")
st.write(f"Percentage of Other Livecoders: {other_count / total * 100:.2f}%")

# Tool usage breakdown
all_tools = [tool for sublist in df['Tool'].apply(eval).tolist() for tool in sublist]
tool_counts = pd.Series(all_tools).value_counts()

st.write("Tool Usage Breakdown:")
st.write(tool_counts)

# Correlation between tools
tool_df = df['Tool'].apply(eval).apply(pd.Series).stack().reset_index(level=1, drop=True).reset_index().rename(columns={0: 'Tool'})
tool_df['Count'] = 1
tool_matrix = tool_df.pivot_table(index='index', columns='Tool', values='Count', fill_value=0)
tool_corr = tool_matrix.corr()

st.write("Tool Correlation Matrix:")
st.write(tool_corr)

# Bar Chart of Categories and Tools
tool_df['Category'] = tool_df['index'].apply(lambda idx: df.loc[idx, 'Category'][0] if isinstance(df.loc[idx, 'Category'], list) else df.loc[idx, 'Category'])
category_tool_counts = tool_df.groupby(['Category', 'Tool']).size().reset_index(name='Count')

fig = px.bar(category_tool_counts, x='Category', y='Count', color='Tool', barmode='group',
             title="Distribution of Tools within Categories")
st.plotly_chart(fig)


# Dialog box for first-time visitors
@st.dialog("Welcome to Livecoding.info!")
def welcome_dialog():
    st.markdown("""
    Welcome to Livecoding.info, a community-driven platform dedicated to showcasing live coding artists from around the world.
    
    ## Features
    - **Artist Categories**: Browse artists categorized by Audio, Visual, and Other tools.
    - **Submit Your Info**: Artists can submit their details using the sidebar form.
    - **Download Data**: Easily download the list of artists in CSV format.
    
    ## How to Get Your Data on the Page
    1. **Submit Your Info**: Use the sidebar form to submit your details. Select your category, tools, and provide other relevant information.
    2. **Pull Request**: Edit the `info.csv` file in [the repository](https://github.com/the-virtual-machine/livecoding.info) and create a pull request with your updates.
    
    Enjoy exploring and connecting with fellow live coders!
    """)
    if st.button("Got it!"):
        st.session_state.visited = True
        st.rerun()

# Show the dialog if the user has not visited before
if 'visited' not in st.session_state:
    welcome_dialog()

