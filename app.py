import streamlit as st

# Import all project components
from frontend.components.sidebar import render_sidebar
from frontend.components.dashboard import render_crop_analytics
from frontend.components.irrigation import render_irrigation_dashboard
from frontend.components.pests import render_pest_management
from frontend.components.quantum_insights import render_quantum_insights
from utils.helpers import load_css

def main():
    """Main application function"""
    # --- Page Configuration ---
    st.set_page_config(
        page_title="🌾 Quantum Smart Farming",
        page_icon="⚛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load Custom CSS from file
    load_css('frontend/styles/custom.css')

    # --- Initialize Session State ---
    if 'quantum_results' not in st.session_state:
        st.session_state.quantum_results = {}

    # --- Render All Components ---
    settings = render_sidebar()

    st.markdown('<h1 class="main-header">🌾 Quantum Smart Farming Dashboard </h1>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌾 Crop Analytics",
        "💧 Irrigation Control",
        "🐛 Pest Management",
        "⚛️ Quantum Insights"
    ])

    # Populate each tab with its dedicated rendering function
    with tab1:
        render_crop_analytics(settings)

    with tab2:
        render_irrigation_dashboard(settings)

    with tab3:
        render_pest_management(settings)

    with tab4:
        render_quantum_insights(settings)

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        f'<div class="footer">Quantum Smart Farming | Built with Qiskit & Streamlit | ⚛️ Powered by {settings["n_qubits"]} Qubits</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()