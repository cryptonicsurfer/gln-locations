import pandas as pd
import folium
import googlemaps
import streamlit as st
from streamlit_folium import folium_static
from io import StringIO

# Initialize Google Maps Client with your API key
gmaps = googlemaps.Client(key=st.secrets['GOOGLE_MAPS_API_KEY'])

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
    
@st.cache_data
def load_data():
    df = pd.read_excel('Copy of GLN-adresser från RD 231115.xlsx')
    df['coordinates'] = df['string_address'].apply(lambda addr: get_gps_coordinates({'street': addr}, addr))
    df['latitude'], df['longitude'] = zip(*df['coordinates'])
    return df



df = load_data()



# Function to convert DataFrame to CSV for download
def convert_df_to_csv(df):
    csv = df.to_csv(index=False)
    return csv

# Add a button to download data
csv = convert_df_to_csv(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='gln_addresses.csv',
    mime='text/csv',
)

