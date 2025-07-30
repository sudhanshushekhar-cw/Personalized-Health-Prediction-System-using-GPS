import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import pandas as pd
import requests
import joblib

# Load your model
model = joblib.load("health_model.pkl")

# Rule-based health risk function
def predict_health_risk(row):
    if row['PM2_5'] > 100 or row['AQI'] > 200:
        if row['RespiratoryCases'] > 7:
            return 'High Risk for Asthma'
    if row['NO2'] > 80 or row['PM10'] > 120:
        if row['CardiovascularCases'] > 5:
            return 'High Risk for Heart Patients'
    return 'Low or Moderate Risk'
  
# Personalized risk based on user profile
def personalized_risk(row, profile):
    risk = []
    if profile['has_asthma'] and row['PM2_5'] > 90:
        risk.append("⚠️ Asthma Risk")
    if profile['has_heart_disease'] and row['NO2'] > 80:
        risk.append("⚠️ Heart Risk")
    if profile['age'] > 60 and row['AQI'] > 150:
        risk.append("⚠️ Senior Risk")
    return ", ".join(risk) if risk else "✅ Safe for your profile"

st.set_page_config(page_title="🌿 Air Quality Health Risk Predictor", layout="wide")

st.title("🌿 Air Quality Health Risk Predictor")
st.markdown("Provide your details and location to get personalized air quality health risk predictions.")

with st.container():
    # Two columns for user inputs side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Your Profile")
        age = st.number_input("Your Age", min_value=1, max_value=120, value=30)
        has_asthma = st.checkbox("Do you have asthma?")
        has_heart_disease = st.checkbox("Do you have heart disease?")
    
    with col2:
        st.subheader("📊 Local Health Data")
        respiratory_cases = st.number_input("Respiratory Cases in your area", min_value=0, value=5)
        cardiovascular_cases = st.number_input("Cardiovascular Cases in your area", min_value=0, value=3)

user_profile = {
    "age": age,
    "has_asthma": has_asthma,
    "has_heart_disease": has_heart_disease
}

st.markdown("---")

# Location detection and manual input
st.subheader("📍 Location Detection")

location = streamlit_geolocation()
if location:
    lat = location.get('latitude')
    lon = location.get('longitude')
    if lat is not None and lon is not None:
        st.success(f"Detected location: {lat:.4f}, {lon:.4f}")
    else:
        st.info("Location detected but latitude or longitude is missing.")
else:
    lat = None
    lon = None
    st.info("Please allow location access or enter manually.")

manual_loc = st.text_input("Or enter location manually (latitude,longitude)")

if manual_loc and (lat is None or lon is None):
    try:
        lat, lon = map(float, manual_loc.split(","))
        st.success(f"Manual location set: {lat:.4f}, {lon:.4f}")
    except:
        st.error("Invalid manual location format. Please enter as latitude,longitude")

st.markdown("---")

if lat is not None and lon is not None:
    if st.button("Get Air Quality and Predict Health Risk"):
        with st.spinner("Fetching data and predicting..."):
            api_key = "15cd56a204a28e7c0dd1792804484fea"
            
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            
            weather_response = requests.get(weather_url)
            air_response = requests.get(air_url)
            
            if weather_response.status_code == 200 and air_response.status_code == 200:
                weather_data = weather_response.json()
                air_data = air_response.json()

                # Extract weather info
                temp = weather_data['main']['temp']  # Celsius
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']

                # Extract air pollution info
                components_data = air_data['list'][0]['components']
                aqi = air_data['list'][0]['main']['aqi']

                input_data = pd.DataFrame([{
                    'PM10': components_data.get('pm10', 0),
                    'PM2_5': components_data.get('pm2_5', 0),
                    'NO2': components_data.get('no2', 0),
                    'SO2': components_data.get('so2', 0),
                    'O3': components_data.get('o3', 0),
                    'Temperature': temp,
                    'Humidity': humidity,
                    'WindSpeed': wind_speed,
                    'AQI': aqi,
                    'RespiratoryCases': respiratory_cases,
                    'CardiovascularCases': cardiovascular_cases
                }])

                  # For demonstration, let's use a sample input data
                # input_data = pd.DataFrame([{
                #     'PM10': 150,                 # High PM10 (above 120)
                #     'PM2_5': 120,               # High PM2.5 (above 100)
                #     'NO2': 90,                  # High NO2 (above 80)
                #     'SO2': 40,                  # Moderate SO2
                #     'O3': 50,                   # Moderate O3
                #     'Temperature': 35,          # Hot weather
                #     'Humidity': 60,             # Humidity moderate-high
                #     'WindSpeed': 1.5,           # Low wind speed
                #     'AQI': 220,                 # Very high AQI (above 200)
                #     'RespiratoryCases': 10,     # High respiratory cases (>7)
                #     'CardiovascularCases': 7    # High cardiovascular cases (>5)
                # }])

                # ML and rule-based prediction
                ml_pred = model.predict(input_data[['PM10','PM2_5','NO2','SO2','O3','Temperature','Humidity','WindSpeed']])[0]
                rule_pred = predict_health_risk(input_data.iloc[0])
                personalized = personalized_risk(input_data.iloc[0], user_profile)

                st.markdown("## 🔍 Prediction Results")
                st.success(f"**ML Prediction (HealthImpactClass):** {ml_pred}")
                st.info(f"**Risk:** {rule_pred}")
                st.info(f"**Personalized Risk:** {personalized}")
            else:
                st.error("Could not fetch weather or air quality data for the location.")

else:
    st.warning("Please provide a valid location (detected or manual) to proceed.")
