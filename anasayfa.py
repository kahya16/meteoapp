import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
# Set config about page
st.set_page_config(
    page_title="Weather App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Hide menu and footer
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

# Load API key from .env file
load_dotenv('/.gitignore')
API_KEY = os.getenv("API_KEY")

# Function to get user's location based on IP
def get_location_by_ip():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data['loc'].split(',')
        lat, lon = float(location[0]), float(location[1])
        return lat, lon
    except Exception as e:
        st.error(f"Error fetching location: {e}")
        return None, None

# Function to get weather data by coordinates
def get_weather_by_coords(lat, lon):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat},{lon}&days=3&aqi=no&alerts=no"
    response = requests.get(url)
    data = response.json()
    return data

# Streamlit app
st.title("🌞 Weathery",anchor=False)
with st.container(border=True):
    st.page_link("pages/1_Find Current Weather.py", label="Other Locations Current Weather", icon="🏞")
# Get user's location
lat, lon = get_location_by_ip()
st.info("Data from https://www.weatherapi.com/")
if lat and lon:
    # Get weather data
    weather_data = get_weather_by_coords(lat, lon)

    if 'current' in weather_data:
        st.subheader(f"Your Location: {weather_data['location']['name']}",anchor=False)
        
        # Display current weather data in columns
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
        st.divider()
        # Display 3-day hourly forecast
        st.subheader("3-Day Hourly Forecast")
        
        cols = st.columns(len(weather_data['forecast']['forecastday']))

        for col, day in zip(cols, weather_data['forecast']['forecastday']):
            with col:
                st.write(f"### {day['date']}")

                # Saatlik verileri bir tabloya dönüştürme
                hourly_data = []
                for hour in day['hour']:
                    hourly_data.append({
                        'Time': hour['time'].split()[1],
                        'Temperature (°C)': f"{hour['temp_c']}°C",
                        'Humidity (%)': f"💧 {hour['humidity']}%",
                        'Wind (km/h)': f" {hour['wind_kph']} km/h",
                        'Condition': f"![]({hour['condition']['icon']})",  # Markdown formatında görsel
                    })

                # Tabloyu DataFrame'e çevir
                df = pd.DataFrame(hourly_data)

                # Tabloyu göster
                st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)
        
    else:
        st.error("Unable to fetch weather data.")
else:
    st.error("Unable to determine your location.")