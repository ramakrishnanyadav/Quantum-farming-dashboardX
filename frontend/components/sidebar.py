import streamlit as st

def render_sidebar():
    """Render the main sidebar with all user controls."""
    st.sidebar.markdown("## ⚛️ Quantum Controls")

    farm_location = st.sidebar.selectbox(
        "🏡 Farm Location",
        ["Maharashtra, India", "California, USA", "Bavaria, Germany", "São Paulo, Brazil"]
    )

    crop_type = st.sidebar.selectbox(
        "🌾 Crop Type",
        ["Wheat", "Corn", "Rice", "Soybeans", "Cotton"]
    )

    st.sidebar.markdown("### Quantum Parameters")
    n_qubits = st.sidebar.slider("Number of Qubits", 2, 6, 4, key="n_qubits")
    circuit_depth = st.sidebar.slider("Circuit Depth (Layers)", 1, 5, 2, key="circuit_depth")
    shots = st.sidebar.slider("Quantum Shots", 512, 4096, 1024, key="shots")

    backend_type = st.sidebar.radio(
        "Quantum Backend",
        ["🖥️ Simulator", "🔬 Fake Device"], # "⚛️ Real Quantum" removed for simplicity
        key="backend_type"
    )

    return {
        'farm_location': farm_location,
        'crop_type': crop_type,
        'n_qubits': n_qubits,
        'circuit_depth': circuit_depth,
        'shots': shots,
        'backend_type': backend_type
    }
