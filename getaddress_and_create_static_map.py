import pandas as pd
import folium
import googlemaps
import streamlit as st
from streamlit_folium import folium_static

# Initialize Google Maps Client with your API key
gmaps = googlemaps.Client(key=st.secrets['GOOGLE_MAPS_API_KEY'])

# Your existing function
def get_gps_coordinates(address, location_name):
    # Check if latitude and longitude are provided
    if address.get('latitude') and address.get('longitude'):
        return address['latitude'], address['longitude']

    # Construct full address string
    full_address = f"{location_name}, {address.get('street', '')}, {address.get('city', '')}, {address.get('zip', '')}"
    geocode_result = gmaps.geocode(full_address)

    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return (None, None)
    
# Read your Excel file into a DataFrame
df = pd.read_excel('Copy of GLN-adresser från RD 231115.xlsx')

# Apply your function to get GPS coordinates for each 'string_address'
df['coordinates'] = df['string_address'].apply(lambda addr: get_gps_coordinates({'street': addr}, addr))

# Separate the coordinates into latitude and longitude
df['latitude'], df['longitude'] = zip(*df['coordinates'])

# Initialize a map at the average location
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

# Add points to the map
for idx, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        folium.Marker([row['latitude'], row['longitude']], popup=row['Namn']).add_to(m)

# Save the map to an HTML file
m.save('map.html')
