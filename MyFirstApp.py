import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time
import os

st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="centered")

st.title("🚗 Car Price Prediction App")
st.write("Welcome! Enter the details below to estimate your car's price.")

# Pull relevant car images from the web
car_options = {
    "Audi A6": "https://cdn.motor1.com/images/mgl/8MMpmx/s1/2024-audi-a6.jpg",
    "BMW 3 Series": "https://cdn.motor1.com/images/mgl/kn6X9/s1/2023-bmw-3-series-sedan-front-view.jpg",
    "Mercedes C-Class": "https://cdn.motor1.com/images/mgl/xBBpY/s1/mercedes-c-class-sedan-front-view.jpg",
    "Toyota Corolla": "https://cdn.motor1.com/images/mgl/6Z8ep/s1/toyota-corolla.jpg",
    "Volkswagen Polo": "https://cdn.motor1.com/images/mgl/vAApN/s1/vw-polo.jpg",
    "Hyundai i20": "https://cdn.motor1.com/images/mgl/1BB8Q/s1/hyundai-i20-front-view.jpg",
    "Ford Figo": "https://cdn.motor1.com/images/mgl/W33gJ/s1/ford-figo.jpg",
}

car_name = st.selectbox("Select Car Model", list(car_options.keys()))
st.image(car_options[car_name], caption=f"{car_name}", use_container_width=True)

# Catergorical Inputs
seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
transmission_type = st.selectbox("Transmission Type", ["Manual", "Automatic"])

# Numerical Inputs
vehicle_age = st.number_input("Vehicle Age (in years)", min_value=0, max_value=30, value=5)
max_power = st.number_input("Max Power (in bhp)", min_value=20.0, max_value=500.0, value=100.0)
engine = st.number_input("Engine Size (in cc)", min_value=500, max_value=5000, value=1500)
km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=50000)
mileage = st.number_input("Mileage (km/l)", min_value=5.0, max_value=50.0, value=18.0)

# Predict Car Price
if st.button("Predict Price"):
    model_path = os.path.join(os.getcwd(), "car_price_model.pkl")

    if not os.path.exists(model_path):
        st.error("❌ Model file not found!")
    else:
        try:
            with st.spinner('🔍 Calculating the estimated price...'):
                time.sleep(2)
                model = joblib.load(model_path)

                input_data = pd.DataFrame([{
                    'seller_type': seller_type,
                    'fuel_type': fuel_type,
                    'transmission_type': transmission_type,
                    'vehicle_age': vehicle_age,
                    'max_power': max_power,
                    'engine': engine,
                    'km_driven': km_driven,
                    'mileage': mileage
                }])

                predicted_price = model.predict(input_data)[0]

            if predicted_price < 0:
                st.error("⚠️ The predicted price is negative. Please check your inputs.")
            else:
                st.success(f"✅ Estimated Price for **{car_name}**: ₹{predicted_price:,.2f}")

        except Exception as e:
            st.error(f"❌ Error during prediction:\n\n{e}")