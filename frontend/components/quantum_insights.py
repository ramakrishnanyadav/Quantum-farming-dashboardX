import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_quantum_insights(settings):
    """Render the educational tab for quantum insights and analytics."""
    st.header("⚛️ Quantum Advantage Analysis")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("🔬 Quantum vs. Classical Performance")
        
        # Sample data for visualization
        comparison_data = {
            'Algorithm': ['Yield Prediction', 'Irrigation Optimization', 'Pest Forecasting'],
            'Classical Accuracy (%)': [82.1, 75.3, 78.9],
            'Quantum Accuracy (%)': [89.7, 87.2, 84.6]
        }
        df_comparison = pd.DataFrame(comparison_data)

        fig = go.Figure(data=[
            go.Bar(name='Classical', x=df_comparison['Algorithm'], y=df_comparison['Classical Accuracy (%)'], marker_color='lightblue'),
            go.Bar(name='Quantum-Enhanced', x=df_comparison['Algorithm'], y=df_comparison['Quantum Accuracy (%)'], marker_color='#00bf63')
        ])
        fig.update_layout(
            barmode='group',
            title_text='Estimated Accuracy Improvement',
            yaxis_title="Accuracy (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("📚 Learn More")
        
        with st.expander("What is Quantum Machine Learning?"):
            st.markdown("""
            Quantum Machine Learning (QML) uses principles of quantum mechanics to solve complex computational problems. 
            - **Superposition**: Qubits can exist in multiple states at once, allowing for massive parallel computation.
            - **Entanglement**: Qubits can be linked, so their fates are intertwined. This helps model complex correlations in data that are impossible for classical computers.
            - **Interference**: Quantum algorithms can amplify the "correct" answers while canceling out "incorrect" ones.
            """)
        
        with st.expander("Why Use it for Farming?"):
            st.markdown("""
            Agriculture is a system with many complex, interacting variables (weather, soil, genetics, markets).
            - **Optimization**: Finding the absolute best irrigation or fertilizer schedule is a massive optimization problem, perfect for algorithms like **QAOA**.
            - **Prediction**: Modeling non-linear relationships, like how soil and weather affect crop yield, can be enhanced by algorithms like **VQR**.
            - **Classification**: Identifying subtle patterns in data to classify pest risk is a good use case for **QSVM**.
            """)