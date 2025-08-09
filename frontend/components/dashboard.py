import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import matplotlib.pyplot as plt

# Import necessary modules
from quantum.algorithms.yield_predictor import QuantumYieldPredictor
from data.collectors.weather_api import WeatherDataCollector
from data.collectors.soil_api import SoilDataCollector # NEW: Import SoilDataCollector
from data.processors.data_loader import load_all_data
from config.settings import FARM_LOCATIONS # NEW: Import FARM_LOCATIONS

def render_crop_analytics(settings):
    """
    Renders the crop analytics tab with live data integration.
    """
    st.header("🌾 Custom Quantum Yield Prediction (VQR)")
    
    # --- Prediction Input ---
    with st.container():
        st.subheader("Prediction Input")
        
        feature_names = ['temperature', 'humidity', 'ph', 'rainfall']
        
        # NEW: Toggle for Live Data
        use_live_data = st.toggle("Use Live Farm Data (Weather & Soil)", key="live_data_toggle")

        current_temp = 25.0
        current_humidity = 65.0
        current_soil_ph = 6.5
        current_rainfall = 50.0

        if use_live_data:
            selected_location_name = settings.get('farm_location', "Maharashtra, India")
            location_coords = FARM_LOCATIONS.get(selected_location_name)

            if location_coords:
                lat = location_coords['lat']
                lon = location_coords['lon']
                city = location_coords['city']

                weather_collector = WeatherDataCollector()
                live_weather = weather_collector.get_live_weather(lat=lat, lon=lon)

                soil_collector = SoilDataCollector() # Instantiate soil collector
                live_soil = soil_collector.get_soil_properties(lat=lat, lon=lon) # Get soil data

                if live_weather and live_soil:
                    st.success(f"Fetched live data for {city}: {live_weather['temperature']}°C, {live_weather['humidity']}% humidity, pH {live_soil['soil_ph']:.1f}.")
                    
                    # Update current values with live data
                    current_temp = live_weather['temperature']
                    current_humidity = live_weather['humidity']
                    current_soil_ph = live_soil['soil_ph']
                    # Rainfall is usually a forecast sum, not current. Use a default or integrate forecast API.
                    # For simplicity, let's derive it or use a default
                    current_rainfall = 50.0 + (live_weather['humidity'] - 65) * 0.5 # Simple heuristic
                else:
                    st.warning("Could not fetch live data from APIs. Using default manual inputs.")
            else:
                st.warning("Location coordinates not found. Using default manual inputs.")
            
            # Display fetched/default values in disabled sliders
            st.slider("🌡️ Temperature (°C)", 10, 50, value=int(current_temp), disabled=True)
            st.slider("💧 Humidity (%)", 0, 100, value=int(current_humidity), disabled=True)
            st.slider("⚗️ Soil pH", 4.0, 8.0, value=current_soil_ph, step=0.1, disabled=True)
            st.slider("🌧️ Rainfall (mm)", 0, 200, value=int(current_rainfall), disabled=True)
            
        else:
            # Manual sliders (enabled)
            current_temp = st.slider("🌡️ Temperature (°C)", 10, 50, 25)
            current_humidity = st.slider("💧 Humidity (%)", 0, 100, 65)
            current_soil_ph = st.slider("⚗️ Soil pH", 4.0, 8.0, 6.5, 0.1)
            current_rainfall = st.slider("🌧️ Rainfall (mm)", 0, 200, 50)
        
        # Button to trigger quantum prediction
        if st.button("Train and Predict Yield", type="primary", key="yield_button"):
            num_qubits = settings.get('n_qubits', 4)
            if len(feature_names) != num_qubits:
                st.error(f"Feature Mismatch: The model requires {len(feature_names)} features, but your sidebar has {num_qubits} qubits selected. Please set 'Number of Qubits' to 4.")
                return

            predictor = QuantumYieldPredictor(num_features=len(feature_names), num_qubits=num_qubits, shots=settings.get('shots', 1024))
            
            with st.spinner("Training Custom VQR model... (This may take a moment)"):
                all_data = load_all_data()
                hist_df = pd.concat([all_data['weather'], all_data['soil'], all_data['crop_yield']], axis=1)
                hist_df = hist_df.rename(columns={'predicted_yield_tons_per_hectare': 'yield'})
                hist_df.dropna(inplace=True)
                
                # Correctly ensure 'ph' column exists from merged 'soil' data
                if 'ph' not in hist_df.columns:
                    st.error("Missing 'ph' column in historical data. Check data/sample_data/soil_data.csv.")
                    return

                train_features = hist_df[feature_names].values
                train_labels = hist_df['yield'].values
                predictor.fit(train_features, train_labels)

            st.success("Model training complete!")

            with st.spinner("Running prediction..."):
                current_features_array = np.array([[current_temp, current_humidity, current_soil_ph, current_rainfall]])
                prediction_array = predictor.predict(current_features_array)
                
                st.session_state.quantum_results['yield'] = {
                    'prediction': prediction_array[0],
                    'circuit': predictor.ansatz.copy()
                }

    # --- Full-Width Results Section ---
    st.divider()

    st.subheader("Prediction Result")
    
    if 'yield' in st.session_state.quantum_results:
        result = st.session_state.quantum_results['yield']
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.metric("Predicted Yield (tons/hectare)", f"{result['prediction']:.2f}")
            
        with res_col2:
            st.info("The circuit below represents the ansatz structure used by the custom VQR.")
            try:
                fig, ax = plt.subplots(figsize=(6, 4))
                viz_circuit = result['circuit']
                viz_circuit.measure_all()
                
                fig.patch.set_facecolor('#FFFFFF00')
                ax.patch.set_facecolor('#FFFFFF00')

                viz_circuit.draw(output='mpl', ax=ax, style={'backgroundcolor': '#EEEEEE'})
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Could not draw circuit: {e}")
    else:
        st.info("Train the model to see a prediction.")