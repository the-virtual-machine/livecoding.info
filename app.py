import streamlit as st
import pandas as pd

# Load the artists' data
artists = pd.read_csv('artists.csv')

# Streamlit app
st.title("Top Livecoding Artists")

for index, artist in artists.iterrows():
    st.header(artist["name"])
    st.subheader(f"From: {artist['from']}")
    st.write(f"Platform: {artist['platform']}")
    st.write(artist["info"])
    
    st.write("Social Media:")
    if pd.notna(artist["social_media_twitter"]):
        st.write(f"[Twitter]({artist['social_media_twitter']})")
    if pd.notna(artist["social_media_instagram"]):
        st.write(f"[Instagram]({artist['social_media_instagram']})")
    st.markdown("---")

st.write("### Add Yourself to the List")
st.write("To add yourself to this list, make a pull request to the [livecoding.info repository](https://github.com/the-virtual-machine/livecoding.info) with your details added to the `artists.csv` file.")
