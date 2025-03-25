import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    # Calculate the result
    return c * r

def main():
    # Page configuration
    st.set_page_config(page_title="Store Locator", page_icon="🏪", layout="wide")
    
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .store-card {
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .store-card h3 {
        margin-top: 0;
        color: #333;
    }
    .store-card p {
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # NIDA Location (starting point)
    NIDA_LAT = 13.771447
    NIDA_LON = 100.654466
    
    # Store data with updated information
    stores = pd.DataFrame({
        "Grocery Brand": [
            "Lotus", 
            "Makro", 
            "CJ MORE", 
            "Foodland"
        ],
        "Store Name": [
            "Lotus Bangkapi", 
            "Makro Ladphrao", 
            "CJ MORE Lat Phrao 130", 
            "Foodland Ladphrao"
        ],
        "Latitude": [
            13.768142, # Lotus
            13.766041, # Makro
            13.772726, # CJ MORE
            13.779413  # Foodland
        ],
        "Longitude": [
            100.643965, # Lotus
            100.640360, # Makro
            100.632133, # CJ MORE
            100.622674  # Foodland
        ],
        "Google Maps Link": [
            "https://maps.app.goo.gl/EodHT737MiJ94B756",
            "https://maps.app.goo.gl/FSKJ8KW8q67878Uk9",
            "https://maps.app.goo.gl/JeaHGM9Jut3ds4F79",
            "https://maps.app.goo.gl/Pe3NRz4X2gjheygA8"
        ],
        "Open Hours": [
            "7:00 AM - 10:00 PM",
            "6:00 AM - 10:00 PM",
            "6:00 AM - 11:00 PM",
            "24 hours"
        ],
        "Telephone": [
            "021165873",
            "023752781",
            "0613875740",
            "025300220"
        ]
    })
    
    # Calculate distances from NIDA
    stores['Distance from NIDA'] = stores.apply(
        lambda row: f"{haversine_distance(NIDA_LAT, NIDA_LON, row['Latitude'], row['Longitude']):.2f} km", 
        axis=1
    )
    
    # Title and introduction
    st.markdown("# Store Locator")
    st.markdown("Find stores near NIDA")
    
    # Create map first, full width
    # Create a folium map
    m = folium.Map(location=[NIDA_LAT, NIDA_LON], zoom_start=13)
    
    # Add NIDA marker with a different color
    folium.Marker(
        location=[NIDA_LAT, NIDA_LON],
        popup="NIDA (Starting Point)",
        tooltip="NIDA",
        icon=folium.Icon(color='green', icon='university')
    ).add_to(m)
    
    # Add store markers
    for _, row in stores.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Store Name']}\nDistance: {haversine_distance(NIDA_LAT, NIDA_LON, row['Latitude'], row['Longitude']):.2f} km",
            tooltip=row["Store Name"]
        ).add_to(m)
    
    # Display the map
    st.markdown("## Store Locations")
    folium_static(m, width=1200, height=600)
    
    # Store details section
    st.markdown("## Store Details")
    
    # Create columns for store cards
    cols = st.columns(2)
    
    # Display store information in card-style boxes
    for i, (_, store) in enumerate(stores.iterrows()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="store-card">
                <h3>{store['Grocery Brand']} - {store['Store Name']}</h3>
                <p><strong>Distance from NIDA:</strong> {store['Distance from NIDA']}</p>
                <p><strong>Open Hours:</strong> {store['Open Hours']}</p>
                <p><strong>Telephone:</strong> {store['Telephone']}</p>
                <p><a href="{store['Google Maps Link']}" target="_blank">View on Google Maps</a></p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()