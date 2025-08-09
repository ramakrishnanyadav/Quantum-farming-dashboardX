import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Import the quantum logic
from quantum.algorithms.irrigation_optimizer import QuantumIrrigationOptimizer

def render_irrigation_dashboard(settings):
    """Render the irrigation optimization tab."""
    st.header("💧 Quantum Irrigation Optimization")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Farm Zone Configuration")
        
        # Use n_qubits from settings to determine the number of zones
        n_zones = settings.get('n_qubits')
        st.info(f"{n_zones} irrigation zones defined by the 'Number of Qubits' in the sidebar.")

        # Create interactive inputs for each zone
        zone_data = []
        for i in range(n_zones):
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input(f"Zone {i+1}", f"Field-{chr(65+i)}", key=f"zone_name_{i}")
            with c2:
                area = st.number_input("Area (ha)", 1.0, 50.0, 10.0, key=f"zone_area_{i}")
            with c3:
                priority = st.selectbox("Priority", ["High", "Medium", "Low"], key=f"zone_priority_{i}")
            
            zone_data.append({
                'name': name,
                'area': area,
                'priority': priority,
                # Simple calculation for water requirement based on priority
                'requirement': area * (5000 if priority == "High" else 3500 if priority == "Medium" else 2500)
            })

        if st.button("⚛️ Optimize Irrigation", type="primary", key="irrigation_button"):
            # Instantiate the optimizer with sidebar settings
            optimizer = QuantumIrrigationOptimizer(settings)
            
            with st.spinner("Running QAOA optimization..."):
                allocation, counts, circuit = optimizer.optimize(zone_data)
                
                st.session_state.quantum_results['irrigation'] = {
                    'allocation': allocation,
                    'zones': zone_data,
                    'counts': counts,
                    'circuit': circuit
                }

        # Display results if they exist
        if 'irrigation' in st.session_state.quantum_results:
            result = st.session_state.quantum_results['irrigation']
            st.success("🎯 Optimization Complete!")

            allocation_df = pd.DataFrame({
                'Zone': [zone['name'] for zone in result['zones']],
                'Allocated Water (L)': result['allocation'],
                'Required Water (L)': [zone['requirement'] for zone in result['zones']]
            })

            fig = go.Figure(data=[
                go.Bar(name='Required', x=allocation_df['Zone'], y=allocation_df['Required Water (L)'], marker_color='lightblue'),
                go.Bar(name='Allocated (Quantum)', x=allocation_df['Zone'], y=allocation_df['Allocated Water (L)'], marker_color='#00bf63')
            ])
            fig.update_layout(title="Quantum-Optimized Water Allocation", barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            # Water savings metric
            total_required = sum(z['requirement'] for z in result['zones'])
            total_allocated = sum(result['allocation'])
            water_saved = total_required - total_allocated
            efficiency = (water_saved / total_required) * 100 if total_required > 0 else 0
            st.metric("💧 Water Efficiency Gain", f"{efficiency:.1f}%", f"~{water_saved/1000:.1f} kL saved")

    with col2:
        st.subheader("⚛️ QAOA Circuit")
        if 'irrigation' in st.session_state.quantum_results:
            circuit = st.session_state.quantum_results['irrigation']['circuit']
            try:
                fig_circ, ax_circ = plt.subplots()
                circuit.draw(output='mpl', ax=ax_circ, style={'backgroundcolor': '#EEEEEE'}, fold=-1)
                st.pyplot(fig_circ)
            except Exception as e:
                st.error(f"Could not draw circuit: {e}")
        else:
            st.info("Run optimization to see the QAOA circuit.")