# frontend/components/quantum_viz.py
def render_quantum_circuit(circuit):
    # Display quantum circuits using qiskit's matplotlib drawer
    fig = circuit.draw('mpl', output='mpl')
    st.pyplot(fig)

def render_quantum_metrics():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Quantum Advantage", "23%", "↑ 5%")
    with col2:
        st.metric("Circuit Depth", "8", "↓ 2")
    with col3:
        st.metric("Fidelity", "94.2%", "↑ 1.2%")

def render_bloch_sphere(statevector):
    # 3D Bloch sphere visualization
    from qiskit.visualization import plot_bloch_multivector
    fig = plot_bloch_multivector(statevector)
    st.plotly_chart(fig)

    def render_quantum_controls():
     st.subheader("⚛️ Quantum Parameters")
    
    n_qubits = st.slider("Number of Qubits", 2, 6, 4)
    ansatz_layers = st.slider("Ansatz Layers", 1, 4, 2)
    optimizer = st.selectbox("Optimizer", ["SPSA", "COBYLA", "ADAM"])
    
    backend_type = st.radio("Backend", 
                           ["Simulator", "Real Quantum (IBM)", "Fake Backend"])
    
    return {
        'n_qubits': n_qubits,
        'ansatz_layers': ansatz_layers,
        'optimizer': optimizer,
        'backend': backend_type
    }