import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static

# Read your CSV file into a DataFrame
df = pd.read_csv('gln_addresses.csv')

# Check if latitude and longitude columns are present and not null
df = df[df['latitude'].notnull() & df['longitude'].notnull()]

# Initialize a map at the average location
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

# Add points to the map
for idx, row in df.iterrows():
    tooltip = f"GLN: {row['GLN']}, Namn: {row['Namn']}, Gatuadress: {row['Gatuadress']}"
    folium.Marker([row['latitude'], row['longitude']], popup=tooltip).add_to(m)

# Save the map to an HTML file
m.save('map.html')

# Display the map in Streamlit
folium_static(m)
