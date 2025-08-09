import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from quantum.algorithms.pest_forecaster import QuantumPestForecaster

def render_pest_management(settings):
    """Render the pest management and risk forecasting tab."""
    st.header("🐛 Quantum-Enhanced Pest Forecasting")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Environmental Risk Factors")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            temp = st.slider("🌡️ Avg Temp (°C)", 10, 45, 28)
        with c2:
            humidity = st.slider("💧 Avg Humidity (%)", 20, 100, 75)
        with c3:
            rainfall = st.slider("🌧️ Recent Rainfall (mm)", 0, 100, 20)
        
        crop_stage = st.selectbox("🌱 Crop Growth Stage", ["Germination", "Vegetative", "Flowering", "Maturation"])

        if st.button("🔍 Analyze Pest Risk", type="primary", key="pest_button"):
            forecaster = QuantumPestForecaster(settings)
            
            # For this simplified model, we only need a few features
            features = np.array([temp, humidity, rainfall])
            
            with st.spinner("Running quantum classification..."):
                risk_score, risk_level, recommendations, circuit, counts = forecaster.forecast(features)
                
                st.session_state.quantum_results['pest'] = {
                    'risk_score': risk_score,
                    'risk_level': risk_level,
                    'recommendations': recommendations,
                    'circuit': circuit,
                    'counts': counts
                }
        
        # Display results
        if 'pest' in st.session_state.quantum_results:
            result = st.session_state.quantum_results['pest']
            
            st.markdown(f"### Risk Assessment: **{result['risk_level']}**")
            
            # Gauge chart for risk score
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['risk_score'] * 100,
                title={'text': "Quantum Risk Score"},
                gauge={'axis': {'range': [None, 100]},
                       'steps': [
                           {'range': [0, 35], 'color': "lightgreen"},
                           {'range': [35, 65], 'color': "yellow"},
                           {'range': [65, 100], 'color': "red"}],
                       'bar': {'color': "black"}}
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.subheader("🎯 Quantum-Generated Recommendations")
            for rec in result['recommendations']:
                st.markdown(f"- {rec}")
    
    with col2:
        st.subheader("⚛️ QSVM-like Circuit")
        if 'pest' in st.session_state.quantum_results:
            circuit = st.session_state.quantum_results['pest']['circuit']
            try:
                fig_circ, ax_circ = plt.subplots()
                circuit.draw(output='mpl', ax=ax_circ, style={'backgroundcolor': '#EEEEEE'}, fold=-1)
                st.pyplot(fig_circ)
            except Exception as e:
                st.error(f"Could not draw circuit: {e}")
        else:
            st.info("Run analysis to see the QSVM-like circuit.")