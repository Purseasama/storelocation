import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import math
from folium.plugins import MarkerCluster

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
    
    # Custom CSS for modern design
    st.markdown("""
    <style>
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', sans-serif;
    }
    .store-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    .store-card:hover {
        transform: translateY(-5px);
    }
    .store-card h3 {
        color: #2c3e50;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .store-card p {
        color: #7f8c8d;
        margin: 5px 0;
    }
    .store-card a {
        color: #3498db;
        text-decoration: none;
        font-weight: 500;
    }
    .store-card a:hover {
        text-decoration: underline;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .stApp {
            padding: 10px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # NIDA Location (starting point)
    NIDA_LAT = 13.771447
    NIDA_LON = 100.654466
    
    # Expanded store data
    stores = pd.DataFrame({
        "Grocery Brand": [
            "CJ MORE", "Foodland", "Makro", "Makro", "Makro", 
            "Makro", "Makro", "Makro", 
            "Lotus", "Lotus", "Lotus", "Lotus", 
            "Lotus", "Lotus", "Lotus", "Lotus", 
            "CJ MORE", "CJ MORE", "CJ MORE", 
            "CJ MORE", "CJ MORE", "CJ MORE"
        ],
        "Store Name": [
            "CJ MORE Lat Phrao 130", "Foodland Ladphrao", 
            "Makro Food Service Ramkhamhaeng", "Makro Food Service Bodindecha", 
            "Makro Food Service Praditmanutham", "Makro Food Service Ramkhamhaeng 24", 
            "Makro Food Service Town in Town", "Makro Ladphrao",
            "Lotus Go Fresh Supermarket Seri Thai", "Lotus Go Fresh, Khlong Chan Housing", 
            "Lotus Bangkapi", "Lotus Go Fresh Ramkhamhaeng (1124)", 
            "Lotus Go Fresh Lat Phrao 130", "Lotus Go Fresh Sukhapiban 1, Khlong Chan", 
            "Lotus Go Fresh Soi Ramkhamhaeng 60", "Lotus Go Fresh Happyland (1828)",
            "CJ MORE Ramkhamhaeng 68", "CJ MORE Khlong Chan Housing", 
            "CJ MORE Lat Phrao 122", "CJ MORE Lat Phrao 112", 
            "CJ MORE Nirun City", "CJ MORE Lat Phrao 107"
        ],
        "Latitude": [
            13.772726, 13.779413, 
            13.776004, 13.770592, 
            13.808937, 13.753660, 
            13.768983, 13.766041,
            13.784872, 13.775958, 
            13.768142, 13.765763, 
            13.771947, 13.770687, 
            13.759247, 13.779997,
            13.764748, 13.776281, 
            13.766826, 13.771893, 
            13.783824, 13.785531
        ],
        "Longitude": [
            100.632133, 100.622674, 
            100.674635, 100.614576, 
            100.618176, 100.625096, 
            100.605658, 100.640360,
            100.673599, 100.649298, 
            100.643965, 100.654282, 
            100.632270, 100.646964, 
            100.650044, 100.643505,
            100.658064, 100.649167, 
            100.623137, 100.619453, 
            100.630808, 100.635811
        ],
        "Google Maps Link": [
            "https://maps.app.goo.gl/JeaHGM9Jut3ds4F79", 
            "https://maps.app.goo.gl/Pe3NRz4X2gjheygA8", 
            "https://maps.app.goo.gl/P8w6ArH1ySTyJz5J8", 
            "https://maps.app.goo.gl/STybc2GNJxJuKB3o8", 
            "https://maps.app.goo.gl/tHwcmTZ1fLpXWouS6", 
            "https://maps.app.goo.gl/z35vGZ3s5QFenCGv9", 
            "https://maps.app.goo.gl/CMWLmpVdWEyLQTdx7", 
            "https://maps.app.goo.gl/FSKJ8KW8q67878Uk9",
            "https://maps.app.goo.gl/wCJ2ryZEcBmBQHNN7", 
            "https://maps.app.goo.gl/VT9YMFDRqQ95wuJU9", 
            "https://maps.app.goo.gl/EodHT737MiJ94B756", 
            "https://maps.app.goo.gl/Q2ZK1vuMhfqcs9pZ9", 
            "https://maps.app.goo.gl/gGs6fU825YBGqDUt9", 
            "https://maps.app.goo.gl/QEBxs57KDVfDQfY17", 
            "https://maps.app.goo.gl/DPfPkgakF82tSaAx6", 
            "https://maps.app.goo.gl/DuzBRyhYY6BrCjTX8",
            "https://maps.app.goo.gl/H4qPLeJX8Q6RyEBb9", 
            "https://maps.app.goo.gl/ursbNg33Hb6WsGaBA", 
            "https://maps.app.goo.gl/3EmpbnKwpkd9N5GM6", 
            "https://maps.app.goo.gl/S6u72YmqwGPyaeaR8", 
            "https://maps.app.goo.gl/NZDfXYKgZy9vY7SG6", 
            "https://maps.app.goo.gl/ow21GzfNFxNjnCdz5"
        ],
        "Open Hours": [
            "6:00-23:00", "24 hours", 
            "6:00-22:00", "6:00-22:00", 
            "6:00-22:00", "6:00-22:00", 
            "6:00-22:00", "6:00-22:00",
            "7:00-21:00", "24 hours", 
            "7:00-22:00", "24 hours", 
            "24 hours", "6:00-22:30", 
            "6:30-22:00", "24 hours",
            "6:00-23:00", "6:00-23:00", 
            "7:00-23:45", "6:00-23:00", 
            "6:00-23:00", "6:00-23:00"
        ],
        "Telephone": [
            "0613875740", "025300220", 
            "020558060", "020217680", 
            "020210210", "020336950", 
            "020063020", "023752781",
            "027319439", "0626057648", 
            "021165873", "", 
            "0626057466", "027979000", 
            "0882340533", "027331265",
            "0646165045", "0642286570", 
            "0613864936", "0613873937", 
            "0613955903", "0613961527"
        ]
    })
    
    # Calculate distances from NIDA
    stores['Distance from NIDA'] = stores.apply(
        lambda row: haversine_distance(NIDA_LAT, NIDA_LON, row['Latitude'], row['Longitude']), 
        axis=1
    )
    
    # Title and introduction with modern styling
    st.markdown("# 📍 Store Location")
    st.markdown("### Find stores near NIDA")
    
    # Create map with modern look
    m = folium.Map(
        location=[NIDA_LAT, NIDA_LON], 
        zoom_start=12, 
        tiles='CartoDB positron'  # Modern, clean map style
    )
    
    # Add NIDA marker with custom icon
    folium.Marker(
        location=[NIDA_LAT, NIDA_LON],
        popup="NIDA (Starting Point)",
        tooltip="NIDA",
        icon=folium.Icon(color='black', icon='user')
    ).add_to(m)
    
    # Color mapping for different grocery brands
    color_map = {
        'Makro': 'red',
        'Lotus': 'green',
        'CJ MORE': 'yellow',
        'Foodland': 'blue'
    }
    
    # Add store markers with detailed popups
    for _, row in stores.iterrows():
        # Determine icon color based on brand
        icon_color = color_map.get(row['Grocery Brand'], 'gray')
        
        # Create a detailed popup HTML
        popup_html = f"""
        <div style='font-family: Arial, sans-serif; min-width: 250px;'>
            <h3 style='color: #2c3e50; margin-bottom: 10px;'>{row['Grocery Brand']} - {row['Store Name']}</h3>
            <p><strong>Distance from NIDA:</strong> {haversine_distance(NIDA_LAT, NIDA_LON, row['Latitude'], row['Longitude']):.2f} km</p>
            <p><strong>Open Hours:</strong> {row['Open Hours']}</p>
            <p><strong>Telephone:</strong> {row['Telephone'] or 'N/A'}</p>
            <a href='{row['Google Maps Link']}' target='_blank' style='color: #3498db; text-decoration: none;'>View on Google Maps</a>
        </div>
        """
        
        # Create a marker with the popup
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row["Store Name"],
            icon=folium.Icon(color=icon_color)
        ).add_to(m)
    
    # Display the map
    st.markdown(" Nearest grocery stores")
    folium_static(m, width=1200, height=600)
    
    # Store details section with categorized columns
    st.markdown("## 📦 Store Details")
    
    # Create 4 columns
    makro_col, lotus_col, cj_col, others_col = st.columns(4)
    
    # Function to display store cards
    def display_store_cards(column, brand_stores):
        with column:
            st.markdown(f"### {brand_stores['Grocery Brand'].iloc[0]} Stores")
            # Sort stores by distance
            sorted_stores = brand_stores.sort_values('Distance from NIDA')
            
            for _, store in sorted_stores.iterrows():
                st.markdown(f"""
                <div class="store-card">
                    <h3>{store['Store Name']}</h3>
                    <p><strong>Distance from NIDA:</strong> {store['Distance from NIDA']:.2f} km</p>
                    <p><strong>Open Hours:</strong> {store['Open Hours']}</p>
                    <p><strong>Telephone:</strong> {store['Telephone'] or 'N/A'}</p>
                    <a href="{store['Google Maps Link']}" target="_blank">View on Google Maps</a>
                </div>
                """, unsafe_allow_html=True)
    
    # Filter and display stores by brand
    display_store_cards(makro_col, stores[stores['Grocery Brand'] == 'Makro'])
    display_store_cards(lotus_col, stores[stores['Grocery Brand'] == 'Lotus'])
    display_store_cards(cj_col, stores[stores['Grocery Brand'] == 'CJ MORE'])
    display_store_cards(others_col, stores[~stores['Grocery Brand'].isin(['Makro', 'Lotus', 'CJ MORE'])])

if __name__ == "__main__":
    main()