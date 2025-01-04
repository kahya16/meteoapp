# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 21:24:15 2024

@author: emiray
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from dotenv import load_dotenv
import os



#Set config about page
st.set_page_config(
    page_title="Current Weather",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        body, .main, .block-container, .css-12oz5g7, .css-1d391kg {
            padding: 15px !important;
            margin: 15px !important;
        }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# WeatherAPI API key
load_dotenv('/.gitignore')

st.title("🌞 Weathery",anchor=False)
API_KEY  = os.getenv("API_KEY")
with st.container(border=True):
    st.page_link("anasayfa.py", label="Home Page", icon="🏠")
#request inf from api
def get_weather_by_coords(lat, lon):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    response = requests.get(url)
    data = response.json()
    return data

st.subheader(f"Other Locations Current Conditions",anchor=False)
st.info("Data from https://www.weatherapi.com/")
# Create Map
m = folium.Map(location=[41.0082, 28.9784], zoom_start=10)  
folium.LatLngPopup().add_to(m)  
clicked_data = st_folium(m, use_container_width=True, height=400)

# Clicked coordinates
try:
    if clicked_data and "last_clicked" in clicked_data:
        lat, lon = clicked_data["last_clicked"]["lat"], clicked_data["last_clicked"]["lng"]
        
        
        
        # Get Data and Show
        weather_data = get_weather_by_coords(lat, lon)
        if "error" not in weather_data:
            # Create metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(label="Temperature", value=f"{weather_data['current']['temp_c']}°C")
            
            with col2:
                st.metric(label="Felt Temperature", value=f"{weather_data['current']['feelslike_c']}°C")
            
            with col3:
                st.metric(label="Humidity", value=f"{weather_data['current']['humidity']}%")
            
            with col4:
                st.metric(label="Wind Speed", value=f"{weather_data['current']['wind_kph']} km/h")
            
            with col5:
                st.write("**Current Condition:**")
                st.image(f"https:{weather_data['current']['condition']['icon']}", width=50)
        else:
            st.error(f"API Error: {weather_data['error']['message']}")
except:
    st.info("Click on map, show weather conditions.")