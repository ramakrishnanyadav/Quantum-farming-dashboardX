import streamlit as st

def load_css(file_name):
    """Loads a CSS file into the Streamlit app for custom styling."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

def show_quantum_badge():
    """Displays a small 'Powered by Quantum' badge."""
    st.markdown(
        '<div style="text-align: right; margin-top: -30px;">'
        '<span style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4);'
        'color: white; padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem;">'
        '⚛️ Quantum Enhanced'
        '</span></div>',
        unsafe_allow_html=True
    )