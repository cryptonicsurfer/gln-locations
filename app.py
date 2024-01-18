import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('gln_addresses.csv')
    return df

def get_marker_color(row, selected_location):
    if row['location_combo'] == selected_location:
        return 'pink'
    else:
        return 'blue'

df = load_data()

# Concatenate string_address and GLN into a new column
df['location_combo'] = df['string_address'] + ' (' + df['GLN'].astype(str) + ')'

# Function to create popup text
def create_popup(row):
    return f"GLN: {row['GLN']}<br>Namn: {row['Namn']}<br>Address: {row['Postbox']}"

# Main area
selected_location = st.selectbox('Sök och välj efter plats:', options=['Visa alla'] + list(df['location_combo'].unique()))

# Initialize map
initial_location = [df['latitude'].median(), df['longitude'].median()]
m = folium.Map(location=initial_location, zoom_start=11)

# Add all markers to the map
for idx, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=create_popup(row),
            icon=folium.Icon(color=get_marker_color(row, selected_location))
        ).add_to(m)

# If a location is selected, recenter map and add its marker on the top layer
if selected_location != 'Visa alla':
    selected_row = df[df['location_combo'] == selected_location].iloc[0]
    if pd.notnull(selected_row['latitude']) and pd.notnull(selected_row['longitude']):
        m.location = [selected_row['latitude'], selected_row['longitude']]
        folium.Marker(
            [selected_row['latitude'], selected_row['longitude']],
            popup=create_popup(selected_row),
            icon=folium.Icon(color='pink', icon='info-sign'),
            zIndexOffset=1000
        ).add_to(m)
        m.zoom_start = 13  # You can adjust this zoom level as needed

# Display the map
colA, colB, colC = st.columns([1,10,1])
with colB:
    folium_static(m, width=1000, height=700,)
